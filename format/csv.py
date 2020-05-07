#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from lib.base import baseclass

import os
import csv
import dotted

class format_csv(baseclass):
    def __init__(self, config, output_config):
        self.filename = os.path.join(config['output_dir'], output_config['filename'])

        if 'unroll' in output_config:
            self.to_unroll = output_config['unroll']
        else:
            self.to_unroll = []
        if 'fields' in output_config:
            self.fields = output_config['fields']
        else:
            self.fields = ["Event.date", "Event.uuid", "Event.info"]
        if 'headers' in output_config:
            self.headers = output_config['headers']
        else:
            self.headers = self.fields

    def generate(self, events, feed_name):
        data = []
        logging.info("Exporting feed {} using screen".format(feed_name))
        for event in events:
            e_feed = event.to_feed(with_meta=True)
            temp_data = []
            for field in self.fields:
                temp = dotted.get(e_feed, field)
                if (isinstance(temp, list) or isinstance(temp, tuple)) and not field in self.to_unroll:
                    temp = ', '.join(temp)
                temp_data.append(temp)
            data.extend(self.unroll(temp_data))
        with open(self.filename, 'w', newline='') as outputfile:
            csvfile = csv.writer(outputfile)
            csvfile.writerow(self.headers)
            for row in data:
                csvfile.writerow(row)
