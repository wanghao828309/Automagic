from pymediainfo import MediaInfo
import os


def video_analysis(file):
    mediainfo = {"v_encoder": None, "res_width": None, "res_height": None, "v_framerate": None, "v_bitrate": None,
                 "v_during": None, "a_encoder": None, "a_channel": None, "a_samplerate": None, "a_bitrate": None,
                 "img_format": None}

    if os.path.isfile(file):
        media_info = MediaInfo.parse(file)
        for track in media_info.tracks:
            if track.track_type == 'Video':
                mediainfo["v_encoder"] = track.format
                mediainfo["res_width"] = track.width
                mediainfo["res_height"] = track.height
                mediainfo["v_framerate"] = track.frame_rate
                mediainfo["v_bitrate"] = track.bit_rate
                mediainfo["v_during"] = track.duration
                # print track.frame_rate_mode
            if track.track_type == 'Audio':
                mediainfo["a_encoder"] = track.format
                mediainfo["a_channel"] = track.channel_s
                mediainfo["a_samplerate"] = track.sampling_rate
                mediainfo["a_bitrate"] = track.bit_rate
            if track.track_type == 'Image':
                mediainfo["v_encoder"] = track.compression_mode
                mediainfo["res_width"] = track.width
                mediainfo["res_height"] = track.height
                mediainfo["img_format"] = track.format
        return mediainfo
    else:
        print "not a file"



def v_video(format, encoder, m_encoder, audioEncoder, m_audioEncoder):
    if format.upper() == "WMV":
        if encoder.upper() == "WMV2":
            assert m_encoder == "WMV2", "encoder !=WMV2"
        else:
            assert m_encoder == "VC-1", "encoder !=VC-1"
        assert m_audioEncoder == "WMA", "audioEncoder !=WMA"

    if format.upper() == "MP4":
        if encoder.upper() == "MPEG-4":
            assert m_encoder == "MPEG-4 Visual", "encoder !=MPEG-4 Visual"
        else:
            assert m_encoder == "AVC", "encoder !=AVC"
        assert m_audioEncoder == "AAC", "audioEncoder !=AAC"

    if format.upper() == "AVI":
        if encoder.upper() == "MPEG-4":
            assert m_encoder == "MPEG-4 Visual", "encoder !=MPEG-4 Visual"
        else:
            assert m_encoder == "JPEG", "encoder !=JPEG"
        assert m_audioEncoder == "MPEG Audio", "audioEncoder !=MPEG Audio"

    if format.upper() == "MOV":
        if encoder.upper() == "MPEG-4":
            assert m_encoder == "MPEG-4 Visual", "encoder !=MPEG-4 Visual"
        else:
            assert m_encoder == "AVC", "encoder !=AVC"
        assert m_audioEncoder == "AAC", "audioEncoder !=AAC"

    if format.upper() == "F4V":
        assert m_encoder == "AVC", "encoder !=AVC"
        assert m_audioEncoder == "AAC", "audioEncoder !=AAC"

    if format.upper() == "MKV":
        if encoder.upper() == "MPEG-4":
            assert m_encoder == "MPEG-4 Visual", "encoder !=MPEG-4 Visual"
        else:
            assert m_encoder == "AVC", "encoder !=AVC"
        assert m_audioEncoder == "AAC", "audioEncoder !=AAC"

    if format.upper() == "TS":
        if encoder.upper() == "MPEG-2":
            assert m_encoder == "MPEG Video", "encoder !=MPEG Video"
        else:
            assert m_encoder == "AVC", "encoder !=AVC"
        assert m_audioEncoder == "MPEG Audio", "audioEncoder !=MPEG Audio"

    if format.upper() == "3GP":
        if encoder.upper() == "MPEG-4":
            assert m_encoder == "MPEG-4 Visual", "encoder !=MPEG-4 Visual"
        else:
            assert m_encoder == "H.263", "encoder !=H.263"
        assert m_audioEncoder == "AAC", "audioEncoder !=AAC"

    if format.upper() == "MPEG-2":
        assert m_encoder == "MPEG Video", "encoder !=MPEG Video"
        assert m_audioEncoder == "MPEG Audio", "audioEncoder !=MPEG Audio"

    if format.upper() == "WEBM":
        assert m_encoder == "VP8", "encoder !=VP8"
        assert m_audioEncoder == "Vorbis", "audioEncoder !=Vorbis"

    if format.upper() == "HEVC":
        assert m_encoder == "HEVC", "encoder !=HEVC"
        assert m_audioEncoder == "AAC", "audioEncoder !=AAC"


def conver_frame(name):
    if name.upper() == "WMV":
        return ("640x480 (4:3 VGA)", "23.97 fps")
    elif name.upper() == "MP4":
        return ("720x480 (NTSC SD)", "24 fps")
    elif name.upper() == "AVI":
        return ("720x576 (PAL SD)", "25 fps")
    elif name.upper() == "MOV":
        return ("1280x720 (16:9 HD)", "29.97 fps")
    elif name.upper() == "F4V":
        return ("1440x1080 (4:3 HD)", "30 fps")
    elif name.upper() == "MKV":
        return ("1920x1080 (16:9 Full HD)", "50 fps")
    elif name.upper() == "TS":
        return ("3840x2160 (16:9 4k UHD)", "59.94 fps")
    elif name.upper() == "3GP":
        return ("4096x2160 (DCI 4K)", "60 fps")
    elif name.upper() == "MPEG-2":
        return ("512x512 (1:1 Square)", "25 fps")
    elif name.upper() == "WEBM":
        return ("2160x3840 (9:16 Portrait)", "30 fps")
    elif name.upper() == "GIF":
        return ("720x1280 (9:16 Portrait)", "25 fps")
    elif name.upper() == "MP3":
        return ("1080x1080 (1:1 Square)", "25 fps")
    elif name.upper() == "HEVC":
        return ("1920x1080 (16:9 Full HD)", "25 fps")



if __name__ == '__main__':
    print video_analysis(r'C:\Users\ws\Desktop\My Video.wmv')