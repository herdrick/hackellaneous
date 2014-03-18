#!/usr/bin/env python -u
# logging user-friendly progress status written to stderr; output is lines of tab-delimited columns written to stdout.
import argparse, sys, os, collections, calendar, datetime, json, itertools, flickrapi
from dateutil import parser as dateutil_parser

api_key = '42ce6cfc281462a7b1c079ebe428bf6b'
flickr = flickrapi.FlickrAPI(api_key, cache=True)


def location_lookup(query):
    print >> sys.stderr, 'looking up location "' + values.location + '"',
    r_find = json.loads(flickr.places_find(query=query, format='json')[14:-1])  # This json is wrapped in a function call, JSONP style. So axe the first 14 chars and last char of the json to get the JSON object within.
    place_id = r_find['places']['place'][0]['place_id']  # this is the flickr place_id  [0] is to get first, most likely result
    place_name = r_find['places']['place'][0]['_content']  # nice string describing location
    return place_id, place_name


def all_photos(place_id, start_datetime, end_datetime, use_cache, tags):
    # day is a datetime
    def one_day_photos(day):
        day_timestamp = calendar.timegm(day.utctimetuple())
        next_day_timestamp = calendar.timegm((day + datetime.timedelta(days=1)).utctimetuple())
        photos = []
        page = 1
        pages = sys.maxint
        while page <= pages:
            print >> sys.stderr, '.',
            filename = 'cache' + '__' + place_id + '__' + day.isoformat(' ').split()[0] + '__' + str(page) + '__' + ('tags' if tags else 'notags') + '.json'
            if use_cache and os.path.isfile(filename):
                with open(filename, 'r') as f:
                    photo_place_json = f.read()
            else:
                photo_place_json = flickr.photos_search(place_id=place_id, min_taken_date=day_timestamp, max_taken_date=next_day_timestamp,
                                                        page=page, per_page='100', extras='date_taken'+(',tags' if tags else ''), format='json')[14:-1]
                with open(filename, 'w') as f:
                    f.write(photo_place_json)
            photo_place_r = json.loads(photo_place_json)
            photos += photo_place_r['photos']['photo']  # there is a list under the key 'photo'. poorly named key.
            pages = photo_place_r['photos']['pages']
            page = page + 1
        return photos

    all_days_photos = []
    date_cursor = start_datetime
    delta = datetime.timedelta(days=1)
    while date_cursor <= end_datetime:
        print >> sys.stderr, '\ngetting statistics about pictures taken on', date_cursor.strftime('%x')
        all_days_photos += one_day_photos(date_cursor)
        date_cursor += delta
    print >> sys.stderr
    return all_days_photos


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Uses the Flickr API to show time statistics for photos taken in a specified location')
    parser.add_argument('location', help='physical location for which to search photos. ex. \'palo alto\'')
    parser.add_argument('--by-tag', action='store_true', default=False, help="separate counts by tag")
    parser.add_argument('--ignore-cache', action='store_true', default=False, help="ignore cache and get fresh results from Flickr API. results will be written to cache (which is a collection of files in the current directory) regardless.")
    parser.add_argument('--date-range', help="date range over which to search photos. ex. '01-20-2014 01-27-2014'. default is previous week.")
    # default date range is the last 7 days
    now = datetime.datetime.utcnow()
    start_datetime = now - datetime.timedelta(days=6)
    default_date_range = start_datetime.isoformat() + ' ' + now.isoformat()
    parser.set_defaults(date_range=default_date_range)
    values = parser.parse_args()
    # get unix timestamps for date range
    start_date, end_date = values.date_range.split()
    start_datetime = dateutil_parser.parse(start_date)
    end_datetime = dateutil_parser.parse(end_date)
    start_timestamp = calendar.timegm(start_datetime.utctimetuple())
    end_timestamp = calendar.timegm(end_datetime.utctimetuple())
    # look up location
    place_id, place_name = location_lookup(values.location)
    print >> sys.stderr, '   using location', place_name
    # get and compile photo stats from API
    all_days_photos = all_photos(place_id, start_datetime, end_datetime, not values.ignore_cache, values.by_tag)
    for phot in all_days_photos:
        phot['datetaken'] = (phot['datetaken'])[:10]  # trim to, ex., '2014-02-14'
    all_days_photos.sort(key=lambda photo: photo['datetaken'])
    # print output to stdout
    if values.by_tag:
        # print counts, grouped by day and tag, to stdout
        date_groups = itertools.groupby(all_days_photos, key=lambda photo: photo['datetaken'])
        for day, one_day_pics in date_groups:
            pics = list(one_day_pics)
            tag_counts = collections.defaultdict(int)
            for pic in pics:
                one_pic_tags = pic['tags'].split()
                one_pic_tags = filter(lambda tag: not ':' in tag, one_pic_tags)
                for tag in one_pic_tags:
                    tag_counts[tag] += 1
            keys = tag_counts.keys()
            keys_set = set(keys)
            for tag, count in sorted(tag_counts.items(), key=lambda item: item[1], reverse=True):
                print '\t'.join([day, tag, str(tag_counts[tag])])  # output
    else:
        # print counts, grouped by day, to stdout
        g = itertools.groupby(all_days_photos, key=lambda photo: photo['datetaken'])
        for key, grp in g:
            print '\t'.join([key, str(len(list(grp)))])  # output
