# Soundcloud OverView

Soundcloud OV is a resume of your year listening music for Soundcloud (Spotify Wrapped but worse).

I doesn't even care about this things like Spotify Wrapped because I hate data collection from big tech companies, but I wanted to make this because people seems to care about how much music they listen and also as a mini project to train myself

I realise that Soundcloud history doesnt track repeated tracks, so if you reproduce a track 2 times only keep track of the last time you listen to this track. So this doesnt work as expected, but at least if was fun :)

# Usage

To install the necesaries python packages run this on terminal

```
$ pip install -r requirements.txt
```

To make your OV you just need: O-Auth and Client ID of Soundcloud and chose your language betweens the diferent output languages of the OV

```
$ python scov.py -o O-Auth -i Client ID -l language
```

This will make and return an html that you can view on your browser

# Disclaimer

I'm not responsible for overuse of Soundcloud API or violation of [Terms of Use of Soundcloud](https://soundcloud.com/terms-of-use)