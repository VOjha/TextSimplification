//
//  TestViewController.swift
//  HMC Word Scroll
//
//  Created by Adam Shaw on 7/1/15.
//  Copyright (c) 2015 HMC LAPDOG. All rights reserved.
//

import UIKit
import Foundation

class TestViewController: UIViewController {
    
    //Initiates the timer and scrollingLabel of the view controller
    var scrollLabel:ScrollingLabel!
    var timer:NSTimer!
    var idNumber:String!
    
    //Start on iteration -1 for acclimation text
    var iteration:Int=(-1)
    
    var masterDataDictionary=Dictionary<String,String>()
    
    //Parameters about screen size
    let scrollLabelHeight:CGFloat=250
    let screenWidth:CGFloat=1024
    let screenHeight:CGFloat=768
    let frameSize:CGFloat=700
    
    //Different types of text
    let textTypes:Array<String>=["Semantics","Syntactic","Lexical"]
    var textVersion:String!
    
    //Randomly picks which version, A or B you will start with
    var versionNumber:Int=Int(arc4random_uniform(2))
    let textVersions:Array<String>=["A","B"]
    
    //The number of texts per text type
    let numberOfTexts:Int=4
    var nextText:String!
    var textType:String!

    var textDictionary:Dictionary<String,String>!

    //Next sample and proceed to MVC respectively
    @IBOutlet weak var softFinishButtonItem: UIButton!
    @IBOutlet weak var hardFinishButtonItem: UIButton!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        hardFinishButtonItem.hidden=true
        createScrollingLabel()
    }
    
    func createScrollingLabel() {
        //Creates the scrollLabel
        scrollLabel=ScrollingLabel(frame: CGRectMake((screenWidth-frameSize)/2,(screenHeight/2)-scrollLabelHeight/2,frameSize,scrollLabelHeight))
        resetScrollingLabelText()
        self.view.addSubview(scrollLabel)
    }
    
    func resetScrollingLabelText() {
        //Resets the position of the scrolling label and changes its text
        scrollLabel.text=getNextText()
        self.timer=NSTimer.scheduledTimerWithTimeInterval(1.0, target: self, selector: Selector("checkForCompletion"), userInfo: nil, repeats: true)
        softFinishButtonItem.hidden=true
        scrollLabel.setContentOffset(CGPointZero,animated:false)
    }
    
    func getNextText() -> String {
        //Determines which text to use next and returns the string of that text
        if iteration==(-1) {
            textType="Acclimation"
        }
        else {
            textType=textTypes[iteration/numberOfTexts]
        }
        let path=NSBundle.mainBundle().pathForResource(textType,ofType:"plist")
        let myDict=NSDictionary(contentsOfFile: path!)
        textDictionary=myDict as! Dictionary<String,String>
        //Switch version every text
        versionNumber=(versionNumber+1)%2
        textVersion=textVersions[versionNumber]
        
        if iteration==(-1) {nextText="1A"}
        else {
            nextText=String((iteration%numberOfTexts)+1)+textVersion
        }
        return textDictionary[nextText]!
    }
    
    func checkForCompletion() {
        //If done with the text, depending on how many texts you have read, reveals a button and adds to the dictionary
        if scrollLabel.doneWithText {
            self.timer!.invalidate()
            if iteration+1==(textTypes.length*numberOfTexts) {
                hardFinishButtonItem.hidden=false
            }
            else {softFinishButtonItem.hidden=false}
            masterDataDictionary["'"+nextText+textType+"'"]=scrollLabel.metricsDictionary.printDict()
        }
    }
    
    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
        //Passes data to MVC
        if segue.identifier=="toMetricsViewController" {
            let mvc=segue.destinationViewController as! MetricsViewController
            mvc.accelerationData=self.masterDataDictionary
            mvc.idNumber=self.idNumber
            
        }
    }
    
    @IBAction func softFinishButton(sender: UIButton) {
        //Resets the label text and moves the scrollLabel to the correct position
        iteration++
        resetScrollingLabelText()
        scrollLabel.restartScrollingLabel()
    }
}




