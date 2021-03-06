#!/usr/bin/env python

from bs4 import BeautifulSoup
import sys
import urllib
import urllib2
import json

package = ""

#Entry point
def searchApp (pack):
    global package
    package = pack
   
#Creates the soup
def createSoup():
    global package
    url = "https://play.google.com/store/apps/details?id=" + package
    try:
        response = urllib.urlopen( url )
    except urllib.error.HTTPError as e:
        print( "HTTPError with: ", url, "\t", e )
        return None
        
    the_page = response.read()
    soup = BeautifulSoup( the_page )   
    
    return soup
    
#Returns the App title
def getAppTitle(display):
    soup = createSoup()
    
    title_div = soup.find( 'div', {'class':'document-title'} )
    title = title_div.find( 'div' ).get_text().strip()
    
    if display:
        print title
        
    return title
    
#Returns the developer name 
def getAppDeveloper(display):
    global package
    soup = createSoup()
    
    subtitle = soup.find( 'a', {'class' : 'document-subtitle primary'} )
    developer = subtitle.get_text().strip()
    dev_link = subtitle.get('href').strip()
    
    if display:
        print developer
        
    return developer
    
#Returns the dev link
def getAppDevLink(display):
    global package
    soup = createSoup()
    
    subtitle = soup.find( 'a', {'class' : 'document-subtitle primary'} )
    developer = subtitle.get_text().strip()
    dev_link = subtitle.get('href').strip()
    
    if display:
        print dev_link
        
    return dev_link
    
#Returns the App updated date    
def getAppUpdateDate(display):
    global package
    soup = createSoup()

    date_published = soup.find( 'div', {'itemprop' : 'datePublished'} )
    updated = date_published.get_text().strip()
    
    if display:
        print updated
    
    return updated
    
#Returns the category
def getAppCategory(display):
    global package
    soup = createSoup()
    
    category_get = soup.find( 'span', {'itemprop' : 'genre'} )
    category = category_get.get_text()
    
    if display:
        print category
    
    return category
    
#Returns the rating
def getAppRating(display):
    global package
    soup = createSoup()
    
    rating_value = soup.find( 'meta', {'itemprop' : 'ratingValue'} )
    rating = rating_value.get( 'content' ).strip()
    
    if display:
        print rating
    
    return rating
    
#Returns reviewers count
def getAppReviewersCount(display):
    global package
    soup = createSoup()
    
    reviewers_count = soup.find( 'meta', {'itemprop' : 'ratingCount'} )
    reviewers = reviewers_count.get( 'content' ).strip()
    
    if display:
        print reviewers
    
    return reviewers
    
#Returns the app badge
def getAppBadge(display):
    global package
    soup = createSoup()
    
    has_badge = soup.find( 'span', {'class' : 'badge-title'} )
    if has_badge: 
        badge = has_badge.get_text().strip()
        
    if display:
        print badge
        
    return badge
    
#Returns the description of the app
def getAppDesc(display):
    global package
    soup = createSoup()
    
    desc = []
    description_div = soup.find_all( 'div', {'class':'id-app-orig-desc'}  )
    for descs in description_div:
        desc.append(descs.get_text().strip())
        
    if display:
        for log in desc:
            print log
        
    return desc

#Returns the app reviews    
def getAppReviews(display):
    global package
    reviews = []
    i = -1
    cur = 0
    while True:
        i += 1
        url = "https://play.google.com/store/getreviews"
        data = "reviewType=0&pageNum=" + str(i) + "&id=" + package + "&reviewSortOrder=4&xhr=1"
        headers = { "orgin" : "https://play.google.com",
                    "accept-language": "en-US,en;q=0.8",
                    "user-agent": "Mozilla/5.0 (X1; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 Safari/537.36",
                    "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
                    "accept": "*/*",
                    "referer": "https://play.google.com/store/apps/details?id="+package}
        req = urllib2.Request(url, data, headers)
        response = urllib2.urlopen(req)
        the_page = response.read()[6:]
        js = json.loads(the_page)
        
        try:
            page = js[0][2]
            if not page:
                raise IndexError
            soup = BeautifulSoup( page )
        except IndexError:
            break

        if not soup: return None
        reviews_div = soup.find_all( 'div', {'class':'single-review'} )
        for review in reviews_div:
            cur += 1
            if display:
             print str(cur)+')', review.find(class_='author-name').get_text().strip(), review.find(class_='tiny-star').get('aria-label').strip(), 'On', review.find(class_='review-date').get_text().strip()
            
            body = review.find(class_='review-body')
            title = body.find(class_='review-title')
            link = body.find(class_='review-link')
            text = title.get_text().strip()
            if display:
                print 'TITLE:', text and text or '(no title)'
            title.decompose()
            link.decompose()
            text = body.get_text().strip()
            reviews.append(text)

            if display:
                print 'REVIEW:', text and text or '(no content)'
                print
        if cur % 20 != 0:
            break

    print 'TOTAL REVIEWS:', cur
    return reviews
    
#Returns the What's new   
def getAppUpdate(display):
    global package
    soup = createSoup()
    
    change = []
    changes_div = soup.find_all( 'div', {'class':'recent-change'}  )
    for changes in changes_div:
        change.append(changes.get_text().strip())
        
    if display:
        for log in change:
            print log
        
    return change
        
#ADDITIONAL INFORMATION

#Returns the size
def getAppSize(display):
    global package
    soup = createSoup()
    
    app_size = soup.find( 'div', {'itemprop' : 'fileSize'} )
    size = app_size.get_text().strip()
    
    if display:
        print size
        
    return size
    
#Returns the number of installs
def getAppInstalls(display):
    global package
    soup = createSoup()
    
    num_downloads = soup.find( 'div', {'itemprop' : 'numDownloads'} )
    if num_downloads: 
        numDownloads = num_downloads.get_text().strip()
        
    if display:
        print numDownloads
        
    return numDownloads

#Returns the App OS
def getAppOS(display):
    global package
    soup = createSoup()
    
    operating_systems = soup.find( 'div', {'itemprop' : 'operatingSystems'} )
    os = operating_systems.get_text().strip()
    
    if display:
        print os
        
    return os

#Returns the maturity content of the app
def getAppMaturity(display):
    global package
    soup = createSoup()
    
    content_rating = soup.find( 'div', {'itemprop' : 'contentRating'} )
    content = content_rating.get_text().strip()
    
    if display:
        print content
        
    return content
    
#Returns the developer links
def getAppDevLinks(display):
    global package
    soup = createSoup()
    
    links = []
    
    for dev_link in soup.find_all( 'a', {'class' : 'dev-link'} ):
        if dev_link.get_text().strip() == "Email Developer":
            email = dev_link.get( 'href' ).strip()[7:]
            links.append(email)
        elif dev_link.get_text().strip() == "Visit Developer's Website":
            dev_website = dev_link.get( 'href' ).strip()
            links.append(dev_website)
            
    if display:
        for link in links:
            print link
        
    return links

def getAppPermissions(display):
    global package
    soup = createSoup()
    
    permission = []
    perms = soup.find_all( 'div', {'class':'permissions-heading'}  )
    print perms
    for perm in perms:
        permission.append(perm.get_text().strip())
        print "hie"
        
    if display:
        for log in permission:
            print log
        
    return permission 
      
if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        print >> sys.stderr, 'SYNTAX: googleplay.py [app-package-name]'
        sys.exit(-1)

    searchApp(args[0])
    getAppCategory(1)
