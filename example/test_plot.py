import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

# img = mpimg.imread('../screenshot/main_page.jpeg')
# img = mpimg.imread('../screenshot/main_page.jpeg')
# img = mpimg.imread('../screenshot/news_normal.jpeg')
# img = mpimg.imread('../screenshot/news_comment.jpeg')
# img = mpimg.imread('../screenshot/comment_comment.jpeg')
# img = mpimg.imread('../screenshot/add_comment.jpeg')

img = mpimg.imread('../autojump.png')

imgplot = plt.imshow(img)
plt.show()