#!/usr/bin/env python
COURSE_URL = 'https://www.memrise.com/course/1123055/russian-4/'
COURSES_URL = 'https://www.memrise.com{}languages/'.format('/courses/english/')
CARD_COLUMNS = ("col_a", "col_b")

import codecs, sys
import os
import re
import requests
from bs4 import BeautifulSoup
from lxml import html
import lxml
import traceback
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from pyvirtualdisplay import Display

def lazy_property(fn):
    """Decorator that makes a property lazy-evaluated.
    """
    attr_name = '_lazy_' + fn.__name__

    @property
    def _lazy_property(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)
    return _lazy_property


def get_soup(url, session = None):
    if session:
        res = session.get(
            url if url.strip().startswith("http") else "http://www.memrise.com" + url)
        soup = BeautifulSoup(res.text, "lxml")
        return soup
    else:
        soup = BeautifulSoup(url, "lxml")
        return soup

class CourseBrowser(object):
    def __init__(self):
        payload = { "username": "MyPySrs", 
                        "password": "MyPySrs", 
                        "csrfmiddlewaretoken": "<TOKEN>"
                        }
        self.session =  requests.session()
        login_url = 'https://www.memrise.com/login/'
        result = self.session.get(login_url)
        tree = html.fromstring(result.text)
        authenticity_token = list(set(tree.xpath("//input[@name='csrfmiddlewaretoken']/@value")))[0]
        payload['csrfmiddlewaretoken'] = authenticity_token

        self.session.post(login_url, data = payload, headers = dict(referer=login_url)) 

        self.courses_url = COURSES_URL
        if __name__ == "__main__": self.browser = webdriver.PhantomJS()
        else: self.browser = webdriver.PhantomJS(executable_path = 'helpLibs/phantomjs.exe')
        self.getLanguages()


    def getLanguages(self):
        availLangs = {}
        soup = get_soup(self.courses_url, self.session)
        soup = soup.find("ul",class_='dropdown-menu')

       
        lis = [x for x in soup if not x == '\n']
        for li in lis:
            availLangs[li.text.strip()] = li.find('a').attrs['href']
       
        self.courses_url = 'https://www.memrise.com{}languages/'.format(availLangs['English'])

        coursesDict = {}
        soup = get_soup(self.courses_url, self.session) 
        soup = soup.find("ul",{'data-default-category-id':'569'})
        #print(soup.find('a').text.strip())
        
        lis = []
        uls = soup
        indent = 0
        count = -1
        for ul in uls:
            if not type(ul.find('a')) is int: lis.append((ul.find('a'), indent))
            try:
                for li in ul.findAll('li'):
                    indent += 1
                    if li.find("span"): indent -= 1; count = len([x for x in [x for x in li.children if not x == '\n'][1].children if not x == '\n']) + 1
                    if count:
                        count -= 1
                    else:
                        count -= 1
                        indent -= 1
                    if not 'data-category-id' in li.attrs: indent += 1
                    if li.find('ul'):
                        lis.append((li.find('a'), indent))
                        if not count:
                            indent += 1
                        continue
                    indent -= 1
                    lis.append((li, indent))
                indent -= 1
            except Exception as e:
                pass#print(traceback.format_exc())
            #indent -= 1

        allCat = {}
        cur1 = None
        cur2 = None
        for li in lis:
            mi = li[0]
            if li[1] == 0:
                if not mi in allCat: allCat[mi] = {}
                cur1 = mi

            if li[1] == 1:
                if not mi in allCat[cur1]: allCat[cur1][mi] = []
                cur2 = mi

            if li[1] == 2:
                if not mi in allCat[cur1][cur2]: allCat[cur1][cur2].append(mi)

        for li in lis:
            mi = li[0]#.text.strip()

            if li[1] == 0:
                cur1 = mi

            if li[1] == 1:
                cur2 = mi
                if len(allCat[cur1][mi]) == 0:
                    allCat[cur1][mi] = []
        self.allCat = allCat

        hrefs = {}
        for i in self.allCat:
            hrefs[i.text.strip()] = i.attrs['href']
            for j in self.allCat[i]:
                try: hrefs[j.text.strip()] = j.find('a').attrs['href']
                except: hrefs[j.text.strip()] = j.attrs['href']
                for k in self.allCat[i][j]:
                    try: hrefs[k.text.strip()] = k.find('a').attrs['href']
                    except: hrefs[k.text.strip()] = k.attrs['href']
        self.hrefs = hrefs

    def loadCourses(self, lang):
        self.courses_url = 'https://www.memrise.com{}'.format(self.hrefs[lang])      
        self.browser.get(self.courses_url)
        self.loadMore()
        
    def loadMore(self):
        canScroll = True
        while canScroll:
            try:
                if not canScroll: break
                button = self.browser.find_element_by_class_name("infinite-scroller-trigger")
                button.click();
                canScroll = False
            except NoSuchElementException as e:
                canScroll = False
            except Exception as e:
                self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def getHtml(self):
        return self.browser.page_source

    def getCourses(self):
        soup = get_soup(self.getHtml())
        featured = soup.find('a',{'class':'featured-course-box'})
        courses = soup.findAll('div', {'class': 'course-box-wrapper'})
        coursesList = [featured]
        for i in courses:
            coursesList.append(i)
        return coursesList

class Course(object):
    def __init__(self, course_url, supLangs):
        self.supLangs = supLangs
        payload = { "username": "MyPySrs", 
                        "password": "MyPySrs", 
                        "csrfmiddlewaretoken": "<TOKEN>"
                        }
        self.session =  requests.session()
        login_url = 'https://www.memrise.com/login/'
        result = self.session.get(login_url)
        tree = html.fromstring(result.text)
        authenticity_token = list(set(tree.xpath("//input[@name='csrfmiddlewaretoken']/@value")))[0]
        payload['csrfmiddlewaretoken'] = authenticity_token

        self.session.post(login_url, data = payload, headers = dict(referer=login_url)) 

        match = re.match(r'^(.*)/(\d+)/?$', course_url)
        if match:
            course_url, level = match.groups()
        else:
            level = None

        self.course_url = course_url
        # a sligle level if it was included in the URL
        self.level = level

    @lazy_property
    def soup(self):
        return get_soup(self.course_url, self.session)

    @property
    def name(self):
        el = self.soup.find("h1", class_="course-name")
        return el.text if el else self.course_url.split('/')[-1]

    @property
    def lang(self):
        el = self.soup.find("div", class_="course-breadcrumb")
        el = el.find_all('a')
        return el[len(el)-1].text.strip()

    @property
    def levels(self):

        #levels = soup.find(lambda tag: tag.name == "div" and "levels" in tag.attrs.get("class"))
        levels = self.soup.find_all("a", class_="level")

        for l in levels:
            url = l.attrs.get("href")
            if self.level and not url.endswith(self.level + '/'):
                continue  ## skip lelevel not requested

            title = l.find("div", class_="level-title").text.strip()
            yield (url, title)


    def cards(self, *, level_url : str):
        """
        :level_url:   level URL
        """
        def get_text(value):
            return '' if value is None else value.text

        soup = get_soup(level_url, self.session)

        for thing in soup.find_all(lambda tag: tag.has_attr("data-thing-id")):
            try:
                cols = (get_text(thing.find("div", class_=col_name).find("div", class_="text")) for col_name in CARD_COLUMNS)
            except:
                continue

            yield cols

    def fix(self):
        linesfromMemrise = self.mylines
        curdate = "{}/{}/{}".format(datetime.now().day,datetime.now().month,datetime.now().year)
        returnlist = []
        #try:
        lenr = len(linesfromMemrise)
        for n,i in enumerate(linesfromMemrise):
            levelcount = 1
            i = i.replace("\n", "")
            i = i.split('\t')
            i[0] = i[0].replace(",", "commaChar")
            i[1] = i[1].replace(",", "commaChar")
            lang = i[4]
            i[4] = '0'
            i.append("0")
            i.append(curdate)
            i.append("none")
            i.append(curdate)
            i.append("0")
            i.append("")
            i.append(i[2])
            i.append(i[3])
            #i[2] = download(i[0])
            i[3] = "no"
            i.append("no")
            i.append(self.supLangs[lang])           
            returnlist.append(i)
        #except Exception as e:
        #   print("dasf", e)
        #   pass
                                
                            
        tmplist = []
        levelcount = 0
        lastLevel = None
        for l in returnlist:
            if l[12] == lastLevel:
                pass
                #l[3] = "Level{}".format(levelcount)
                #tmplist.append(",".join(l))
            else:
                lastLevel = l[12]
                levelcount += 1
            l[12] = "Level{}".format(levelcount)
            tmplist.append(",".join(l))
        self.newCourse = tmplist

    def dump_course(self):
        """
        :course_url:   course URL
        """
        mylines = []
        lNum = 1
        valid = False
        if len([(x,y) for x,y in self.levels]) > 0:
            for level_url, title in self.levels:
                for card in self.cards(level_url=level_url):
                    ent ='\t'.join(card).split('\t')
                    if not ent[0] == '' and not ent[1] == '':
                        #print("\t".join([ent[0], ent[1], course.name, 'Level{}'.format(lNum), course.lang]))
                        mylines.append("\t".join([ent[0], ent[1], self.name, 'Level{}'.format(lNum), self.lang]).replace(',','commaChar'))
                        valid = True
                    else: valid = False
                if valid:
                    lNum += 1
        else:
            for card in self.cards(level_url=self.course_url):
                ent ='\t'.join(card).split('\t')
                if not ent[0] == '' and not ent[1] == '':
                    #print(",".join([ent[0], ent[1], course.name, 'Level{}'.format(lNum), course.lang]))
                    mylines.append("\t".join([ent[0], ent[1], self.name, 'Level{}'.format(lNum), self.lang]).replace(',','commaChar'))
                    valid = True
                else: valid = False
            if valid:
                lNum += 1
        self.mylines = mylines

# t = CourseBrowser()
# t.loadCourses()
# print(t.getCourses()[1])