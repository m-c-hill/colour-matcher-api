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

*Example*:

```
curl -X 'POST' \
  'http://0.0.0.0:8000/v1/images/match-colour' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "url": "https://pwintyimages.blob.core.windows.net/samples/stars/test-sample-teal.png"
}'
```

*Response*:

```
{
  "url": "https://pwintyimages.blob.core.windows.net/samples/stars/test-sample-teal.png",
  "matched_colour": "tropical_rain_forest"
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

<grey_image>


**Teal**

<teal_image>


## Future Improvements
- Optimisation of pixel search
- Experiment with maximising the compression of each image
- ... # TODO before interview

## References

CompuPhase, 2019. *Colour metric*. Available from: https://www.compuphase.com/cmetric.htm [Accessed 17 Oct 2022].
