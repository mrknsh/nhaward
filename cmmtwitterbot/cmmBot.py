# -----------------------------
# COLLEGE MEDIA MADNESS BOT
# Bot to live tweet results from the college media madness fundraiser on the @mediamadness22 account
# Written by Mark Nash for The Daily Orange
# marknash@dailyorange.com / it@dailyorange.com
# -----------------------------

# IMPORTS
from distutils.command.upload import upload
import tweepy
import gspread
import requests
from PIL import Image, ImageDraw, ImageFont
import sys
import math
import time
import os
from datetime import datetime
from datetime import timedelta

# API + CONFIG
# need this for linux
dirPath = os.path.dirname(os.path.realpath(__file__))
# Load config
nextMilestone = 0
dayOfComp = 0
# config file structure: nextMilestone,dayOfComp
with open(dirPath + '/config.txt') as c:
    configLine = c.readlines()[0]
    configParts = configLine.split(",")
    nextMilestone = int(configParts[0])
    dayOfComp = int(configParts[1])

# Authenticate to Twitter
TWITTER_API_KEY = "xxx"
TWITTER_API_KEY_SECRET = "xxx"
TWITTER_ACCESS_TOKEN = "xxx"
TWITTER_ACCESS_TOKEN_SECRET = "xxx"
twitterAuth = tweepy.OAuth1UserHandler(
   TWITTER_API_KEY, TWITTER_API_KEY_SECRET,
   TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
)
twitterAPI = tweepy.API(twitterAuth)
twitterAPI.verify_credentials()

# Authenticate to Google
gc = gspread.service_account()
# Open the sheet from a spreadsheet with the results
resultsSheet = gc.open("College Media Madness 2022").sheet1

# font path needs to be in the os fonts dir
fontPath = "Viga-Regular.ttf"

# HELPER FUNCTIONS
# createTotalGFX
    # Function
        # Takes amount of money to put on graphic
        # Returns location of created graphic in the gfx/outputs folder
    # EOD/Milestone Total GFX Creation Notes:
        # Template Location - gfx/templates/cmm_milestone.jpg
def createTotalGFX(amount):
    # load in template parts
    font = ImageFont.truetype(font = fontPath, size = 218)
    template = Image.open(dirPath + "/gfx/templates/cmm_milestone.jpg")

    # parse amount into string
    amountString = "$" + str('{:,}'.format(int(amount)))

    # place that string on the template
    draw = ImageDraw.Draw(template)
    # calculate the size of the text
    tW, tH = draw.textsize(amountString, font=font)
    # TODO: catch for the text being too wide
    draw.text((600 - tW / 2 , 20), amountString, (253, 173, 13), font=font)

    # save this image
    outName = "milestone_" + str(int(time.time()))
    outPath = "gfx/outputs/" + outName + ".jpg"
    template.save(dirPath + "/" + outPath) 

    # return our file path
    return outPath

# createTopGFX
    # Function
        # Takes list of 5 top papers and puts on graphic
        # Returns location of created graphic in the gfx/outputs folder
    # EOD/Milestone Total GFX Creation Notes:
        # Template Location - gfx/templates/cmm_top5.jpg
def createTopGFX(topPapers):
    # if the number of top papers are greater than 5 throw a fit
    if len(topPapers) > 5:
        sys.exit(6)

    # load in template image and fonts
    paperRankFont = ImageFont.truetype(font = fontPath, size = 50)
    paperNameFont = ImageFont.truetype(font = fontPath, size = 50) 
    paperAmountFont = ImageFont.truetype(font = fontPath, size = 50)
    template = Image.open(dirPath + "/gfx/templates/cmm_top5.jpg")
    draw = ImageDraw.Draw(template)

    # draw text
    # we have 628 pixels of height to draw each of the papers
    # that is ~ 125 pixels of height per paper
    # we have 850 pixels of width to draw each paper
    # breakdown by height top down:
        # 17.5 pixels of buffer
        # 90 pixels for paper
        # 17.5 pixels of buffer
    # breakdown by width inside to out:
        # starting at x = 435
        # 10 pixels inside the right edge (i.e right edge at x = 1190) (and 50 pixels tall in the middle vertically of the unit): amount
        # 50 pixels outside of right edge of left logo area (i.e x = 400) (same vert as amount ^): rank
    # loop paper by paper
    for x in range(len(topPapers)):
        vStart = 125 * x #how far down to start drawing
        # draw rank
        rankString = str(x + 1) + "."
        tW, tH = draw.textsize(rankString, font=paperAmountFont)
        rankW = tW
        draw.text((400, vStart + 37.5), rankString, (138, 150, 202), font=paperRankFont) 
        # draw amount
        amountString = "$" + str('{:,}'.format(int(topPapers[x][3])))
        tW, tH = draw.textsize(amountString, font=paperAmountFont)
        amountW = tW
        draw.text(((1190 - tW), vStart + 37.5), amountString, (253, 173, 13), font=paperAmountFont)
        # figure out how much space we have to work with for the paper name
        space = (1190-400) - rankW - amountW - 30 # 30 is the buffer for the paper name (10 on left side) 

        # draw paper name
        paperName = topPapers[x][1]
        tW, tH = draw.textsize(paperName, font=paperNameFont)
        fontSize = paperNameFont.size
        while tW > space:
            # whole tW is bigger than space keep making the font smaller
            fontSize -= 5
            paperNameFont = ImageFont.truetype(font = fontPath, size = fontSize)
            tW, tH = draw.textsize(paperName, font=paperNameFont)
        # now that we have the font right we can draw
        draw.text(((400 + rankW + 10), vStart + 37.5), paperName, (0, 0, 0), font=paperAmountFont)


    # save this image
    outName = "top_" + str(int(time.time()))
    outPath = "gfx/outputs/" + outName + ".jpg"
    template.save(dirPath + "/" + outPath) 

    # return our file path
    return outPath

# tweetEODTotal
    # Function
        # Takes amount donated and the day of the competition
        # Tweets the graphic with text and returns the ID of the tweet
        # Called in conjection with replyCTA function
    # Tweet Notes:
        # Tweet: At the end of day <day of competition>, $<amount raised> has been raised for student journalism via College Media Madness 2022!
def tweetEODTotal(amount, day):
    # make text
    tweetText = "At the end of day " + str(day) + ", $" + str('{:,}'.format(int(amount))) + " has been raised for student journalism via College Media Madness 2022!"
    # upload image that we get from the create function, we want the ID
    imagePath = createTotalGFX(amount)
    media = twitterAPI.media_upload(dirPath + "/" + imagePath)
    # tweet but we also need to get the tweet ID so we can return it
    tweetID = twitterAPI.update_status(status=tweetText, media_ids=[media.media_id])
    return tweetID.id

# tweetMilestone
    # Function
        # Takes a milestone number
        # Tweets about said milestone and returns the ID of the tweet
        # Called in conjection with replyCTA function
    # Tweet Notes:
        # Tweet: We have passed the $<milestone> mark of money raised for student journalism
def tweetMilestone(milestone):
    tweetText = "We have passed the $" +  str('{:,}'.format(int(milestone))) + " mark of money raised for student journalism"
    # make and upload image
    imagePath = createTotalGFX(milestone)
    media = twitterAPI.media_upload(dirPath + "/" + imagePath)
    # tweet but we also need to get the tweet ID so we can return it
    tweetID = twitterAPI.update_status(status=tweetText, media_ids=[media.media_id])
    return tweetID.id

# tweetTopPaper
    # Function
        # Takes a list of 5 top papers and the day of the competition
        # Tweets about the top papers and returns the ID
        # Called in conjection with replyCTA function
    # Tweet Notes:
        # Tweet: Check out the top 5 student media organizations going into day <day> of College Media Madness!
def tweetTopPapers(topPapers, day):
    tweetText = "Check out the top 5 student media organizations going into day " + str(day) + " of College Media Madness!"
    # make and upload image
    imagePath = createTopGFX(topPapers)
    media = twitterAPI.media_upload(dirPath + "/" + imagePath)
    # tweet but we also need to get the tweet ID so we can return it
    tweetID = twitterAPI.update_status(status=tweetText, media_ids=[media.media_id])
    return tweetID.id

# replyCTA
    # Function
        # Takes a tweet ID to reply to
        # Replies to the tweet with a call to action
    # Tweet Notes:
        # Tweet: Help support student journalism. Donate today at collegemediamadness.com
        # Don't need to include @ sign as we are auto populating
def replyCTA(tweetID):
    # reply to the tweet with the CTA
    # you need the @ or the auto_populate_reply_metadata=true
    tweetText = "Help support student journalism. Donate today at collegemediamadness.com"
    twitterAPI.update_status(status = tweetText, in_reply_to_status_id = tweetID, auto_populate_reply_metadata=True)
    return True


# DATA PROCESSING
# Pull the data and put it into a list of tuples
# (School Name, Paper Name, Total Donors, Amount Raised)
# gspread -> cell B1 = (1, 2)
# build a list and also track totals
results = []
totalAmountRaised = 0
totalDonors = 0
# get cols like this to cut down on API calls
schoolNames = resultsSheet.col_values(1)
paperNames = resultsSheet.col_values(4)
numberDonors = resultsSheet.col_values(7)
amounts = resultsSheet.col_values(6)
for x in range(1, len(schoolNames)):
    # data needs to be cleaned of $ and ,
    schoolName = str(schoolNames[x])
    paperName = str(paperNames[x])
    donorCount = int(str(numberDonors[x]).replace("$","").replace(",",""))
    amountRaised = float(str(amounts[x]).replace("$","").replace(",",""))
    schoolData = (schoolName, paperName, donorCount, amountRaised)
    # append totals
    totalDonors += int(str(numberDonors[x]).replace("$","").replace(",",""))
    totalAmountRaised += float(str(amounts[x]).replace("$","").replace(",",""))
    # add to list
    results.append(schoolData)

# sort data by amount raised (last item of tuple)
results = sorted(results, key=lambda i: i[-1], reverse=True)


# DO TWEETS BASED ON CIRCUMSTANCES
# Morning - Top Papers
# tweet morning top papers if we are in MTP mode don't do the morning stuff on day 1
if len(sys.argv) > 1 and sys.argv[1] == "mtp" and dayOfComp > 1:
    topPapers = results[0:5]
    # run tweets
    # first get ID of the first tweet
    tweetID = tweetTopPapers(topPapers, dayOfComp)
    # then reply with the CTA
    replyCTA(tweetID)

# End of Day - Recap
# tweet end of day totals if we are in EOD mode
if  len(sys.argv) > 1 and sys.argv[1] == "eod":
    # run tweets
    # first get ID of the first tweet
    tweetID = tweetEODTotal(totalAmountRaised, dayOfComp)
    # then reply with the CTA
    replyCTA(tweetID)

    # increase the daysIntoCompetition number bc this is running at the end of the day
    configFile = open(dirPath + "/" + "config.txt","w")
    configFile.truncate(0)
    dayOfComp += 1
    configFile.write(str(nextMilestone) + "," + str(dayOfComp))

# Anytime - Milestones
# tweet for a milestone if we hit one
if totalAmountRaised >= nextMilestone:
    # if we got past more than one milestone tweet that
    # run tweets
    # first get ID of the first tweet
    tweetID = tweetMilestone(nextMilestone)
    # then reply with the CTA
    replyCTA(tweetID)

    # increase the next milestone by $5,000
    configFile = open(dirPath + "/" + "config.txt","w")
    configFile.truncate(0)
    nextMilestone = int(math.ceil(totalAmountRaised / 5000.0) * 5000.0)
    configFile.write(str(nextMilestone) + "," + str(dayOfComp))
