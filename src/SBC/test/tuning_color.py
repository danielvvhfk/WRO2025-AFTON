import cv2
import numpy as np

def calculate_hsv_range(image_path):
    """
    Calculate the HSV color range for an image.
    :param image_path: Path to the image file.
    :return: lower and upper HSV bounds as numpy arrays.
    """
    # Load the image
    image = cv2.imread(image_path)
    
    # Convert the image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Calculate the minimum and maximum HSV values for the image
    lower_bound = np.min(hsv_image, axis=(0, 1))  # Minimum values across the image
    upper_bound = np.max(hsv_image, axis=(0, 1))  # Maximum values across the image
    
    # Return the HSV range
    return lower_bound, upper_bound

def main():
    # File paths for the red and green cropped images
    red_image_path = 'red.png'
    green_image_path = 'green.png'
    
    # Calculate HSV ranges for red and green
    lower_red, upper_red = calculate_hsv_range(red_image_path)
    lower_green, upper_green = calculate_hsv_range(green_image_path)
    
    # Print the results
    print("Red HSV Range:")
    print("Lower bound:", lower_red)
    print("Upper bound:", upper_red)
    
    print("\nGreen HSV Range:")
    print("Lower bound:", lower_green)
    print("Upper bound:", upper_green)
    
    # Optionally save the results to a file for easy copying
    with open("tuned_color_ranges.txt", "w") as f:
        f.write(f"Red HSV Range:\nLower: {lower_red}\nUpper: {upper_red}\n\n")
        f.write(f"Green HSV Range:\nLower: {lower_green}\nUpper: {upper_green}\n")
    
if __name__ == "__main__":
    main()
