//
//  MetricsViewController.swift
//  HMC Word Scroll
//
//  Created by Adam Shaw on 7/1/15.
//  Copyright (c) 2015 HMC LAPDOG. All rights reserved.
//

import UIKit
import MessageUI

class MetricsViewController: UIViewController, MFMailComposeViewControllerDelegate {
    //Sends off the data in an email, if available
    
    var accelerationData:Dictionary<String,String>!
    var idNumber:String!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        if MFMailComposeViewController.canSendMail() {
            let emailer = MFMailComposeViewController()
            emailer.mailComposeDelegate=self
            emailer.setSubject("ID Number: \(idNumber)")
            emailer.setMessageBody(accelerationData.printDict(),isHTML:false)
            emailer.setToRecipients(["text.difficulty.data.hmc@gmail.com"])
            self.presentViewController(emailer,animated:true,completion:nil)
        }
    }
    
    func mailComposeController(controller: MFMailComposeViewController, didFinishWithResult result: MFMailComposeResult, error: NSError?) {
        controller.dismissViewControllerAnimated(true, completion: nil)
    }
}