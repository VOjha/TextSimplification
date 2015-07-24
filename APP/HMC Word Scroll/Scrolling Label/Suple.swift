//
//  Suples.swift
//  MedeRead v0.2
//
//  Created by Adam Shaw on 6/8/15.
//  Copyright (c) 2015 Adam Shaw. All rights reserved.
//

import Foundation

struct Suple<A:Hashable,B:Hashable>:Hashable,Equatable,CustomStringConvertible {
    //A tuple like object which may hold two items
    var itemA:A
    var itemB:B
    
    init (_ itemA:A,_ itemB:B) {
        self.itemA=itemA
        self.itemB=itemB
    }
    
    var hashValue: Int {
        return itemA.hashValue^itemB.hashValue
    }
    
    var description: String {
        return "(\(itemA), \(itemB))"
    }
    
}

func ==<A,B> (lhs:Suple<A,B>,rhs:Suple<A,B>) -> Bool {
    return lhs.itemA==rhs.itemA && lhs.itemB==rhs.itemB
}














