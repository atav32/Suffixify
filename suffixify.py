import json
import argparse
import pythonwhois
import sys
import time


def parse_args():
  parser = argparse.ArgumentParser(description='Search for available domains')
  parser.add_argument('keywords', nargs='+', help='A keyword to search around')
  args = vars(parser.parse_args())
  return args


def load_suffixes():
  with open('suffixes.json') as data_file:
    suffixes = json.load(data_file)
  return suffixes


def append_suffixes(keywords, suffixes):
  domain_names = []
  for keyword in keywords:
    keyword_suffixes = [keyword + suffix for suffix in suffixes]
    domain_names.extend(keyword_suffixes)

  domains = [domain_name + '.com' for domain_name in domain_names]
  return domains


def loop_through_domains(domains):
  for domain in domains:
    try:
      details = pythonwhois.get_whois(domain)
      if details['contacts']['registrant'] is None:
        print domain, 'Available!'
    except Exception as e:
      print domain, e
    time.sleep(1)


def main(argv):
  args = parse_args()
  suffixes = load_suffixes()
  domains = append_suffixes(args['keywords'], suffixes)
  loop_through_domains(domains)


if __name__ == "__main__":
  main(sys.argv)
