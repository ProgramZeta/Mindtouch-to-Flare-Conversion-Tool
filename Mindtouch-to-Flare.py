import argparse
import urllib2
import os
from lxml import etree

argument_parser = argparse.ArgumentParser(description='Convert a Mindtouch wiki to a Flare project')
argument_parser.add_argument('-i', dest='interactive_mode', help='force interactive mode', action='store_true')
argument_parser.add_argument('-u', '--url', help='url of a mindtouch wiki system')
argument_parser.add_argument('-o', '--output', help='local directory to store the new help system (default: current directory)')
args = argument_parser.parse_args()

print "Mindtouch Wiki to Flare Project Conversion Tool"

def interactive_mode():
    try:
        url = get_url()
        directory = get_directory()
    except:
        raise
    return [url, directory]

def get_url():
    url_is_ok = False
    while not url_is_ok:
        print "Please provide the front-page URL of the help system (example: http://www.example.com/wiki/):"
        url = raw_input("URL: ")
        try:
           url = verify_url(url)
           url_is_ok = True
        except:
            if raw_input("Error while verifying url, continue? ") in {"no", "n", "No", "N"}:
                raise
        else:
            return url

def get_directory():
    directory_is_ok = False
    while not directory_is_ok:
        print "Please provide the local directory where you want to save the Flare project to (leave blank for current directory):"
        directory = raw_input("Directory: ")
        try:
           directory = verify_directory(directory)
        except:
            if raw_input("Error while verifying directory, continue? ") in {"no", "n", "No", "N"}:
                raise
        else:
            return directory

def verify_url(url):
    # Make sure we have a url
    if url == "":
        return False
    # Make sure our URL is in the correct format 
    # Should start with http
    if url.split("://")[0] != "http":
        print "Adding 'http://' to the beginning of the url"
        url = "http://" + url
    # Should have ending slas
    if url[len(url)-1] != "/":
        print "Adding '/' to end of URL"
        url = url + "/"

    # See if we can contact the root site
    try:
        print "Accessing " + url
        f = urllib2.urlopen(url)
        print "Successfully accessed " + url
    except urllib2.URLError, e:
        print e
        raise
    except urllib2.HTTPError, e:
        print e
        raise
    except:
        print "Unknown error accessing " + url
        raise
        
    # Check to see if the Mindtouch API is available
    mindtouch_api_url = url + "@api/deki"
    try:
        print "Accessing " + mindtouch_api_url
        urllib2.urlopen(mindtouch_api_url)
        print "Successfully accessed " + url
    except urllib2.URLError, e:
        print e
        raise
    except urllib2.HTTPError, e:
        print e
        raise
    except:
        print "Unknown error accessing " + url
        raise
    return url

def verify_directory(directory):
    if directory == "":
        directory = os.getcwd()
    if os.access(directory, os.W_OK):
        print "Able to access " + directory
        return directory
    else:
        print "Unable to access " + directory
        if raw_input("Try to create " + directory + "? ") in {"Yes", "yes", "Y", "y"}:
            try:
                os.makedirs(directory)
                os.access(directory, os.W_OK)
            except os.error, e:
                print e
                raise
            except:
                print "Unknown error occurred when trying to create " + directory
                raise
            else:
                return directory
        else:
            raise StandardError
        
# Program entry point
url = args.url
directory = args.output 
if args.interactive_mode == True:
    try:
        results = interactive_mode()
    except:
        print "Error occured, help system was not converted."
        sys.exit(1)
    else:
        url = results[0]
        directory = results[1]
else:
    try:
        url = verify_url(url)
        directory = verify_directory(directory)
    except:
        print "Error occured, help system was not converted."
        sys.exit(1)


print "Beginning content download"

# Go through the page listing, and start grabbing from each page
try:
    page_listing_url = url + "@api/deki/pages"
    page_listing = urllib2.urlopen(page_listing_url)
except Exception, e:
    print "Error when accessing Mindtouch wiki page list"
    print e

try:
    page_url = ""
    page_title = ""
    for event, element in etree.iterparse(page_listing, events=("start", "end")):
        if element.tag == "page" and event == "start":
            if "href" in element.attrib:
                page_title = ""
                page_url = unicode(element.attrib["href"], "ascii")
        if element.tag == "title" and event == "end":
            page_title = element.text
        if page_url != "" and page_title != "":
            print "Creating topic file " + page_title.encode('utf-8')
            try:
                pass
            except:
                print "Error creating "
            print "Accessing " + page_url.encode('utf-8')
            try:
                pass
            except:
                pass
            print " "
            page_url = ""
            page_title = ""
except Exception, e:
    print "Error when parsing page list"
    raise



# Create a new topic
# Add the starting html tags
# Set the title as the first <h1> tag in the topic
# Copy the contents
# Add the ending tags
# Fix the links
# Copy the images locally
