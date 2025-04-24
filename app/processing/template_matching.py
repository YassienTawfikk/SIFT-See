import cv2
import numpy as np

class TemplateMatching:

    @staticmethod
    def match_template(image, template, method="NCC"):

        output=image #initialize
        # Convert image and temp to grayscale if needed
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        if len(template.shape) == 3:
            template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

        #image and template dimensions
        img_h, img_w = image.shape
        h, w = template.shape

        if method=="SSD":
            #initialize ssd array (assume no padding and that template is completely inside the image)
            ssd_map = np.zeros((img_h - h + 1, img_w - w + 1), dtype=np.float32)

            # Slide the window and calculate SSD
            for y in range(ssd_map.shape[0]):
                for x in range(ssd_map.shape[1]):
                    window = image[y:y + h, x:x + w]
                    diff = (window.astype(np.float32) - template.astype(np.float32))
                    ssd = np.sum(diff ** 2)
                    ssd_map[y, x] = ssd  #stores the SSD value for the window whose top-left corner is at (x, y).

            # Find the position with minimum SSD
            min_loc = np.unravel_index(np.argmin(ssd_map), ssd_map.shape)   #gives coordinates as in (y,x) ---> row,col

            top_left = min_loc[::-1]  # switch coordinates order to be (x, y) --> col, row
            bottom_right = (top_left[0] + template.shape[1], top_left[1] + template.shape[0])
            cv2.rectangle(output, top_left, bottom_right, (0, 0, 255), 2)

        elif method=="NCC":
            ncc_map = np.zeros((img_h - h + 1, img_w - w + 1), dtype=np.float32)

            # Precompute template normalization terms
            template = template.astype(np.float32)
            template_mean = np.mean(template)
            template_centered = (template - template_mean)

            for y in range(ncc_map.shape[0]):
                for x in range(ncc_map.shape[1]):
                    window = image[y:y + h, x:x + w].astype(np.float32)
                    window_mean = np.mean(window)
                
                    window_centered = (window - window_mean)

                    #build NCC equation
                    numerator = np.sum(window_centered * template_centered)
                    denominator = np.sqrt(np.sum(window_centered ** 2) * np.sum(template_centered ** 2))

                    ncc_map[y, x] = numerator / denominator

            # Find location of max NCC (best match)
            max_loc = np.unravel_index(np.argmax(ncc_map), ncc_map.shape)
            top_left = max_loc[::-1]
            bottom_right = (top_left[0] + w, top_left[1] + h)
            cv2.rectangle(output, top_left, bottom_right, (0, 255, 0), 2)

        return output