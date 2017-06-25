#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from app import create_app
import logging

app = create_app()

if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s %(message)s',
        datefmt='%Y/%m/%d %H:%M:%S',
        level=logging.INFO)
    app.run(host="0.0.0.0", port=9011, debug=False)
