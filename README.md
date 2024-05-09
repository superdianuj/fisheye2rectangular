# Dual Fisheye to Equirectangular Projection Mapping

```bash
python processor2.py --dir
```

The method used for mapping is a rather crude pixel-by-pixel conversion. You
can clearly see the 'stitch' where the two images are joined together. You can
probably achieve much better results with software that actually 'blends'
together the images, like [hugin](http://hugin.sourceforge.net/), but that's
also a bit more complicated ;).
