from scrapper import nHentai
import argparse

parser = argparse.ArgumentParser(description='nhentai-download')
parser.add_argument('id', type=int, help='nhentai id')
parser.add_argument('concurrent_count', type=int, nargs='?', default=20, help='how many to download at the same time')
args = parser.parse_args()

# yes
