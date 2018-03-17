def convert_microsecond_to_player_time(micro_second):
    total_seconds = micro_second // 10**6
    
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    if hours == 0:
        return '%d:%02d:%02d' % (hours, minutes, seconds)
    else:
        return '%02d:%02d' % (minutes, seconds)
