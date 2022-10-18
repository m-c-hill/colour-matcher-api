# Colour Matcher API

Colour Matcher takes an image URL and returns the colour that the image as a whole matches most closely from a palette of over 800 distinct colours. The application was written using [FastAPI](https://fastapi.tiangolo.com/).

## Getting Started

### Run the App

```
docker build . -t colour_matcher
docker run -p 8000:80 colour_matcher
```

### Run the Tests

```
./run-tests.sh
```

## REST API

**POST** `/v1/images/match-colour`

Submit a URL containing an image in PNG, JPEG or JPG format. Returns the name of the dominant colour found in the image.

_Example_:

```
curl -X 'POST' \
  'http://0.0.0.0:8000/v1/images/match-colour' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "url": "https://pwintyimages.blob.core.windows.net/samples/stars/test-sample-teal.png"
}'
```

_Response_:

```
{
  "url": "https://pwintyimages.blob.core.windows.net/samples/stars/test-sample-teal.png",
  "matched_colour": "skobeloff"
}
```

If an invalid URL containing no image content is sent in the request body, the response will contain a 422 status code and the following message:

```
{
    "detail": "URL contains no valid image content."
}
```

## Colour Matching

### Theory

Colours can be represented using the [RGB colour model](https://en.wikipedia.org/wiki/RGB_color_model), an additive model in which each colour is represented by the combination three integers (0-255), each of these representing the additive primary colours: red, green and blue.

To calculate the difference between two colours, it should be as simple as just calculating the Euclidean distance between two RGB points in three-dimensional space.

![image](https://user-images.githubusercontent.com/74383191/196426805-a6b3bbaf-c625-47bc-8a88-a7165de3605e.png)

However, the RGB model does not accurately model the non-linear way in which humans perceive colour. A low-cost algorithm for determining colour difference is the [redmean formula](https://www.compuphase.com/cmetric.htm), which is a weighted Euclidean distance function, where the square differences between each colour component are weighted as a funtion of the mean red level in both colours:

![image](https://user-images.githubusercontent.com/74383191/196426868-bd762533-27cf-4357-b4da-8f5a2ff2af74.png)

### Algorithm

Using the redmean formula, the Colour Matcher application works in the following way:

1. Confirm that the input URL contains a valid JPEG, JPG or PNG image.
2. Download and compress the image, adding the resultant rows of RGB pixels to an array.
3. Retrieve the palette of predefined colours from the SQLite database.
4. Create a dictionary cache to store pixels that have already been analysed `{(r,g,b): "matched_colour"}`.
5. Create a dictionary to count the frequency of matched colours `{"colour": freq}`.
6. Cycle through each pixel in the compressed image array.
7. If the pixel RGB tuple is present in the cache, continue to next pixel. Otherwise, calculate the redmean colour difference between the pixel and each colour in the palette, tracking the colour with the minimum difference. Add this pixel RGB value and colour match to the cache.
8. After analysing each pixel, find the matched colour with the highest frequency (usning the dictionary in step 4).
9. Check that this colour is the dominant colour in the image (percentage of pixels matching this colour must exceed the defined threshold of 30%).
10. Return the name of the matched colour.

### Postman Screenshot

Example of POST request in [Postman](https://www.postman.com/) for grey and teal images:

**Grey**

![image](https://user-images.githubusercontent.com/74383191/196459088-3669c00b-8742-4777-8114-74e256b96e95.png)

![image](https://user-images.githubusercontent.com/74383191/196459663-b1e36f40-19eb-4f3a-819e-1cb33e09be48.png)

**Teal**

![image](https://user-images.githubusercontent.com/74383191/196458957-9c8b9285-fedf-4ed1-bca2-672b6d7f3d5e.png)

![image](https://user-images.githubusercontent.com/74383191/196458859-beec3ec3-28f2-4182-9559-f837314afc51.png)

## Future Improvements

#### 1. Optimise the Compression of Images

- The time complexity for the algorithm is currently O(N\*C), where N is the number of pixels and C is the number of colours in the palette.
- The speed of the algorithm used to match a colour to an image is relatively quick for images composed of few colours. This is because pixels with matching RGB values are only analysed once. Once a pixel is matched, it is cached such that future pixels of equal RGB values can then retrieve the closest colour from the cache, rather than having to go through the full colour palette analysis.
- It is therefore vitally important to reduce both the number of pixels that need to be analysed and the number of unique colours in the image being processed.
- An attempt has been made to reduce the number of pixels using the `PIL` library's `size` method to compress the image.
- This compression could perhaps be optimsed using [octree color quantization](https://observablehq.com/@tmcw/octree-color-quantization) to reduce the number of unique colours in the image before processing. The [Python Imaging Library contains the `quantize()` method](https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Quantize.FASTOCTREE) to achieve this.

#### 2. Optimise Pixel Colour Matching Using Nearest Neighbour

- Currently, when matching a pixel, the algorithm performs a linear serach, sweeping through the entire stored palette of over 800 known colours.
- A [nearest neighbour algorithm using a k-d tree](https://blog.krum.io/k-d-trees/) would have been a more efficient approach as it allows for entire batches of colours to be disregarded in a single operation. However, given the time contraints of this assignment and the difficulty in combining this with the redmean equation, it has not been attempted at the present time.

#### 3. API Features & Data Models

- Option to remove colours from the palette (ie. matching images while ignoring a background colour such as white).
- Ability to define and input colour dominance threshold (see `services.py`).
- Add option for a 'redmean matching threshold' (ie. for a colour to match, its redmean difference must be within the range of a certain threshold, otherwise the match is not valid).
- Add a cache timeout to previously run queries stored in the database. Currently, the endpoint will check if the URL has been processed previously and return that result if found in the `images` table. If the image cache record is older than a given period of time and the URL is resubmitted, the image should be fully reprocessed rather than drawing from the cache. This will account for situations where URLs are resubmitted but their associated image resource has perhaps been updated.

#### 4. System Design

- More extensive testing, especially unit tests.

## References

CompuPhase, 2019. _Colour metric_. Available from: https://www.compuphase.com/cmetric.htm [Accessed 17 Oct 2022].
