import re
import os
import argparse
from xml.etree.ElementTree import ElementTree

DEBUG = False
#DEBUG = True

class Rule:
    """A regex that may indicate a security problem, and some associated information."""
    """Element is an Element object, derived from XML file"""
    def __init__(self, element):
        if element.tag == "Rule":
            self.title = element.findtext("Title")
            self.severity = element.findtext("Severity")
            self.type = element.findtext("Type")
            self.guidance = element.findtext("Guidance")
            self.description = element.findtext("Description")
            self.extensions = []
            for ext in element.find("Extensions").findall("Extension"):
                self.extensions.append(ext.text)
            #trueExamples are expressions that should match the regex 
            self.trueExamples = []
            if check_false_neg and element.find("RealPositiveExamples") is not None:
                for ex in element.find("RealPositiveExamples").findall("Example"):
                    self.trueExamples.append(ex.text)
            #falseExamples are expressions that should *not* match regex,
            #although actually eliminating false positives is more aspiration than realistic goal
            self.falseExamples = []
            if check_false_pos and element.find("FalsePositiveExamples") is not None:
                for ex in element.find("FalsePositiveExamples").findall("Example"):
                    self.falseExamples.append(ex.text)
            self.regExString = element.findtext("RegularExpressionPattern")
            self.regEx = re.compile(self.regExString, re.IGNORECASE)
        else:
            #TODO: Have actual error-handling here, probably an exception
            print "Invalid XML"
    def ruleTester(self):
        """make sure our regexes work the way we want them to"""
        print "Now testing rule: " + self.title + "\nWith regex: " + self.regExString + "\n"
        if check_false_neg:
            for ex in self.trueExamples:
                if not self.regEx.search(ex):
                    print "\tFail: regex did not match:\n\t" + ex + "\n"
        if check_false_pos:
            for ex in self.falseExamples:
                if self.regEx.search(ex):
                    print "\tFail: regex incorrectly matched:\n\t" + ex + "\n"
        return

def getRulesInFile(file):
    if DEBUG:
        print "now parsing: " + file
    XML = ElementTree()
    XML.parse(file)
    #TODO: actually handle error
    if XML.getroot().tag != "Rules":
        print "Invalid XML"
    ruleNodes = XML.findall("Rule")
    allRules = []
    for node in ruleNodes:
        allRules.append(Rule(node))
    return allRules
    
def getAllRules(dir="../Rules"):
    allRules = []
    for r,d,f in os.walk(dir):
        for file in f:
            if file.endswith(".xml"):
                allRules.extend(getRulesInFile(os.path.join(r,file)))
    return allRules

        
#get some command line options
parser = argparse.ArgumentParser(description='Test whether YASAT rules are matching what we want them to.Checks for false positives and false negatives by default.')
parser.add_argument('-n', action="store_true", default=False, help='Only check false negatives')
parser.add_argument('-p', action="store_true", default=False, help='Only check false positives')
args = parser.parse_args()

check_false_neg = args.n
check_false_pos = args.p


#default is to check both
if not(check_false_neg or check_false_pos):
    check_false_neg = check_false_pose = True


rules = getAllRules()

for rule in rules:
    rule.ruleTester()
