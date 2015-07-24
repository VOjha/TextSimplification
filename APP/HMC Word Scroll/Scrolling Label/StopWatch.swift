//
//  StopWatch.swift
//  ScrollingLabel
//
//  Created by Adam Shaw on 6/4/15.
//  Copyright (c) 2015 Adam Shaw. All rights reserved.
//

import Foundation

struct StopWatch {
    //A structure which emulates a typical stopwatch
    private var startTime: NSDate?
    private var accumulatedTime: NSTimeInterval=0.0
    
    var elapsedTime: NSTimeInterval {
        get {
            return self.accumulatedTime+NSDate().timeIntervalSinceDate(self.startTime ?? NSDate())
        }
    }
    
    mutating func start() {
        startTime=NSDate()
    }
    
    mutating func stop() {
        accumulatedTime += NSDate().timeIntervalSinceDate(self.startTime ?? NSDate())
        startTime=nil
    }
    
    func timeIntervalToString() -> String? {
        //Outputs the time in a user friendly Minutes:Seconds format.
        let dcf = NSDateComponentsFormatter()
        dcf.zeroFormattingBehavior = .Pad
        dcf.allowedUnits = ([.Minute, .Second])
        return dcf.stringFromTimeInterval(self.elapsedTime)
    }
    
}