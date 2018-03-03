#!/usr/bin/env python
COURSE_URL = '/course/128133/dirty-russian-by-native-russian-speaker/'
COURSES_URL = 'https://www.memrise.com/courses/english/languages/'
CARD_COLUMNS = ("col_a", "col_b")

import codecs, sys
import os
import re
import requests
from bs4 import BeautifulSoup
from lxml import html
import traceback

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


def get_soup(url, session):
    res = session.get(
        url if url.strip().startswith("http") else "http://www.memrise.com" + url)
    soup = BeautifulSoup(res.text, "html.parser")
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
        self.getLanguages()

    def getLanguages(self):
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
        cur3 = None
        for li in lis:
            mi = li[0]#.text.strip()
            #print('\t' * li[1] + li[0].text.strip())
            if li[1] == 0:
                if not mi in allCat: allCat[mi] = {}
                cur1 = mi

            if li[1] == 1:
                if not mi in allCat[cur1]: allCat[cur1][mi] = []
                cur2 = mi

            if li[1] == 2:
                if not mi in allCat[cur1][cur2]: allCat[cur1][cur2].append(mi)
                cur3 = mi

        for li in lis:
            mi = li[0]#.text.strip()

            if li[1] == 0:
                cur1 = mi

            if li[1] == 1:
                cur2 = mi
                if len(allCat[cur1][mi]) == 0:
                    allCat[cur1][mi] = None
        
        #finished = False
        #relo = {}
        #cur = [soup]
        #test = []
        #sibs = []
        # while len(cur) > 0:
        #     try:
        #         t = len(cur)-1
        #         for i in [x for x in cur[len(cur)-1].children if not x == '\n']:
        #             cur.append(i)
        #             #test.append(i)
        #             try:
        #                 lasti = i.text.strip();
        #                 if not '\n' in lasti:
        #                     #print(relo[lasti], lasti)
        #                     #if not mi in relo[lasti]: relo[lasti][mi] = {}
        #                     #print(lasti)
        #                     #lasti = i.text.strip()
        #                     sibs = []
        #             except Exception as e: print(e)
        #         del cur[t]
        #     except Exception as e:
        #         relo[lasti] = cur[t].strip()
        #         test.append(cur[t])
        #         del cur[t]
            
        
        #print(relo)
            

            


        #for i in soup.children:
        #    print(i)
                    

                #if not str(j) == "\n": print(j.prettify(), '1')
            #for j in soup.find('li'):
             #   print(i,j)
            #for col in row.find_all('a'):
             #   print(row, col)

        #while len(soupSearch[len(soupSearch) - 1]) > 0:

         #   soupSearch.append(soupSearch[len(soupSearch) - 1].find('a'))
            
            # try:
            #     if not i.string.strip() == "":
            #         if not i.string.strip() in coursesDict:
            #             coursesDict[i.string.strip()] = []
            # except:
            #     pass
            # for j in i:
            #     try:
            #         coursesDict[i.string.strip()].append(j.string.strip())
            #     except:
            #         pass
        #print(coursesDict)

class Course(object):
    def __init__(self, course_url):
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

def dump_course(*, course_url : str):
    """
    :course_url:   course URL
    """
    course = Course(course_url=course_url)
    mylines = []
    lNum = 1
    valid = False
    if len([(x,y) for x,y in course.levels]) > 0:
        for level_url, title in course.levels:
            for card in course.cards(level_url=level_url):
                ent ='\t'.join(card).split('\t')
                if not ent[0] == '' and not ent[1] == '':
                    print(",".join([ent[0], ent[1], course.name, 'Level{}'.format(lNum), course.lang]))
                    mylines.append(",".join([ent[0], ent[1], course.name, 'Level{}'.format(lNum), course.lang]))
                    valid = True
                else: valid = False
            if valid:
                lNum += 1
    else:
        for card in course.cards(level_url=course_url):
            ent ='\t'.join(card).split('\t')
            if not ent[0] == '' and not ent[1] == '':
                print(",".join([ent[0], ent[1], course.name, 'Level{}'.format(lNum), course.lang]))
                mylines.append("\t".join([ent[0], ent[1], course.name, 'Level{}'.format(lNum), course.lang]))
                valid = True
            else: valid = False
        if valid:
            lNum += 1
    return mylines


def main(url):
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    course_url = COURSE_URL if len(sys.argv) < 2 else sys.argv[1]
    return dump_course(course_url=url)

t = CourseBrowser()