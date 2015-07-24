//
//  Extensions.swift
//  ScrollingLabel
//
//  .fraCreated by Adam Shaw on 6/4/15.
//  Copyright (c) 2015 Adam Shaw. All rights reserved.
//

import Foundation
import UIKit
import QuartzCore

extension UITextView {
    var fontSize: CGFloat {
        //Allows the font size of the textView to be directly accessible
        get {
            return self.font!.fontSize
        }
        set(newValue) {
            self.font=UIFont(name: self.font!.fontName, size: newValue)
        }
    }
}

extension UIFont {
    var fontSize: CGFloat {
        //Gives pointSize a more apt name
        return self.pointSize
    }
}

extension UIView {
    func addSubview(scrollingLabel:ScrollingLabel) {
        //Allows the scrollingLabel to be easily added to a master view
        self.addSubview(scrollingLabel.baseScrollView)
    }
}

extension Array {
    var length:Int {
        return self.count
    }
}

extension String {
    var words:Array<String> {
        //Finds distinct words within a master string separated by " " or "\n"
        let items=self.componentsSeparatedByCharactersInSet(NSCharacterSet.whitespaceAndNewlineCharacterSet())
        var words:[String]=[]
        for word in items {
            if word.rangeOfCharacterFromSet(NSCharacterSet.letterCharacterSet()) != nil{
                words.append(word)
            }
        }
        return words
    }
    
    var wordCount:Int {
        //Creates a more usable name
        return self.words.count
    }
    
    var averageWordLength: Double {
        //Finds the length of the average word in a string
        let concatenatedWords="".join(self.words)
        let totalCharLength=concatenatedWords.length
        return Double(totalCharLength)/Double(self.wordCount)
    }
    
    var length:Int {
        //Gives a more recognizable name
        return self.characters.count
    }
    
    func findWordsBeforeIndex(index:Int) -> Int {
        //Returns the number of complete words before a certain character index
        let index:String.Index=advance(self.startIndex,index)
        let substring=self.substringToIndex(index)
        return substring.wordCount-1
        //slight bug: should only return wordCount-1 when the last character is from a truncated string
    }
}

extension UILabel {
    func addBorder(color:UIColor) {
        //Debugger tool to find label borders
        self.layer.cornerRadius=5
        self.layer.masksToBounds=true
        self.layer.borderColor=color.CGColor
        self.layer.borderWidth=4
    }
    
    var fontSize: CGFloat {
        //Allows fontSize to be readable/writeable
        get {
            return self.font.fontSize
        }
        set(newValue) {
            self.font=UIFont(name: self.font.fontName, size: newValue)
        }
    }
    
    var fontName: String {
        //Allows the fontName to be writable/mutate the font itself
        get {
            return self.font.fontName
        }
        set(newName) {
            self.font=UIFont(name: newName, size: self.font.fontSize)
        }
    }
}

extension NSTimeInterval {
    func format(formatInt:Int) -> String {
        //Allows formatting to a certain decimal point
        let floatVersion=Float(self)
        return floatVersion.format(formatInt)
    }
}

extension Float {
    func format(formatInt:Int) -> String {
        //Truncates the float after a certain decimal point/
        let numberFormatter = NSNumberFormatter()
        numberFormatter.minimumFractionDigits=formatInt
        numberFormatter.maximumFractionDigits=formatInt
        return numberFormatter.stringFromNumber(self) ?? "\(self)"
    }
}

extension Dictionary {
    func printDict() -> String {
        //Returns a python-friendly description format
        var stringToReturn="{"
        for (key,value) in self {
            stringToReturn+="\(key): \(value), "
        }
        stringToReturn=String(dropLast(dropLast(stringToReturn.characters)))
        stringToReturn+="}"
        return stringToReturn
    }
}








