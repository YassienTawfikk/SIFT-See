import cv2
import numpy as np

class TemplateMatching:

    @staticmethod
    def match_template(image, template):

        output=image #initialize
        
        # Convert image and temp to grayscale if needed
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        if len(template.shape) == 3:
            template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

        #determine dimensions
        img_h, img_w = image.shape
        h, w = template.shape
        
        #initialize ssd array (assume no padding)
        ssd_map = np.zeros((img_h - h + 1, img_w - w + 1), dtype=np.float32)

        # Slide the window and calculate SSD
        for y in range(ssd_map.shape[0]):
            for x in range(ssd_map.shape[1]):
                window = image[y:y + h, x:x + w]
                diff = (window.astype(np.float32) - template.astype(np.float32))
                ssd = np.sum(diff ** 2)
                ssd_map[y, x] = ssd

        # Find the position with minimum SSD
        # min_val = np.min(ssd_map)
        min_loc = np.unravel_index(np.argmin(ssd_map), ssd_map.shape)   #as in (y,x)

        # output = image.copy()
        top_left = min_loc[::-1]  # (x, y)
        bottom_right = (top_left[0] + template.shape[1], top_left[1] + template.shape[0])
        cv2.rectangle(output, top_left, bottom_right, (0, 0, 255), 2)

        return output

        # return min_loc, min_val, ssd_map

    # # Example usage:
    # image = cv2.imread('image.jpg')
    # template = cv2.imread('template.jpg')

    # loc, val, ssd_map = template_match_ssd(image, template)
    # print(f"Best match at location: {loc} with SSD: {val}")

    # # Optional: visualize result
    # output = image.copy()
    # top_left = loc[::-1]  # (x, y)
    # bottom_right = (top_left[0] + template.shape[1], top_left[1] + template.shape[0])
    # cv2.rectangle(output, top_left, bottom_right, (0, 0, 255), 2)