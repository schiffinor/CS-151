# Proj 4
# Stephanie Taylor
# spring 2011

import graphicsPlus


def displayImage(src, title):
    '''Open a new window, give it the specified title,
    and display the image
    Input:
        src : a Zelle Image
        title : a string
    Output:
        the window in which the pixmap is displayed
    '''

    # get the size of the image
    w = src.getWidth()
    h = src.getHeight()

    # create a graphics window that is the size of the image
    win = graphicsPlus.GraphWin(title, w, h)

    # center the image in the window.
    # take the location you want it (w/2, h/2)
    # and subtract the location where it is (getAnchor)
    # then move the image so it is centered in the window
    dx = w/2 - src.getAnchor().getX()
    dy = h/2 - src.getAnchor().getY()
    src.move(dx, dy)

    # draw the image into the window
    src.draw(win)

    # done, return a reference to the window
    return win
