#!/usr/bin/env python

## Example of execution: knn.py ../data/train.dat ../data/test.dat

import sys, logging, os
from optparse import OptionParser


## Reads corpus and creates the appropiate data structures:
def read_corpus(file_name):
    f = open(file_name, 'r')

    ## first line contains the list of attributes
    attr = {}
    ind = 0
    for att in f.readline().strip().split("\t"):
        attr[att] = {'ind': int(ind)}
        ind += 1

    ## the rest of the file contains the instances
    instances = []
    ind = 0
    for inst in f.readlines():
        inst = inst.strip()

        elems = inst.split("\t")
        if len(elems) < 3: continue

        instances.append({'values': list(map(int, elems[0:-1])),
                          'class': int(elems[-1]),
                          'index': int(ind),
                          })
        ind += 1
    ## Print Tests
    ##for i in instances: 
        ##print(list(i['values'])) 
    ##for i in instances: 
        ##for j in i['values']: 
            ##print(j) 
    ##print(list(instances[0]['values'])) 
    return attr, instances


def get_closest_instance(inst, instances):
    ## so far we don't know the closest instance
    closest_instance = None
    ## we are looking for the smallest instance, so initialize to a big number
    prev_distance = float("inf")
    instance1 = list(inst['values'])
    ##print(len(instances))
    ##sys.exit()
    ## loop through all instance in instances and get the closest one to inst
    for instance in instances:
        distance = 0
        ## STEPS:
        ## 1.- calculate the distance between inst and instance
        ## Note - I'm using the Hamming Distance because it is equivalent to the Minkowski/Manhattan distance for binary attributes. 
        instance2 = list(instance['values'])  
        assert len(instance1) == len(instance2)
        for idx,val in enumerate(instance1): 
            print("inside loop")
            if val != instance2[idx]: 
                distance += 1
        ## 2.- if the distance is less than prev_distance,
        ##       update closest instance and prev_distance
        if distance < prev_distance: 
            prev_distance = distance 
            closest_instance = instance 
            

    ## 3.- return closest_instance
    ## Right now we are always returning the first instance from instances,
    ##   which is probably not the closest one to inst.
    ##   Your job is to get the closest one and return it
    return closest_instance


def calculate_accuracy(instances, predictions):
    predictions_ok = 0
    for i in range(len(instances)):
        if instances[i]["class"] == predictions[i]:
            predictions_ok += 1

    return 100 * predictions_ok / float(len(instances))


if __name__ == '__main__':
    usage = "usage: %prog [options] TRAINING_FILE TEST_FILE"

    parser = OptionParser(usage=usage)
    parser.add_option("-d", "--debug", action='store_true',
                      help="Turn on debug mode")

    (options, args) = parser.parse_args()
    if len(args) != 2:
        parser.error("Incorrect number of arguments")
    if not os.path.isfile(args[0]):
        parser.error("Training file does not exist\n\t%s" % args[0])
    if not os.path.isfile(args[1]):
        parser.error("Training file does not exist\n\t%s" % args[1])

    if options.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.CRITICAL)

    file_tr = args[0]
    file_te = args[1]
    logging.info("Training: " + file_tr)
    logging.info("Testing: " + file_te)

    ## (I)  Training: read instances
    attr_tr, instances_tr = read_corpus(file_tr)

    ## (II) Testing: read instances and
    ##      predict the class of the closest instance in training
    attr_te, instances_te = read_corpus(file_te)
    predictions = []
    ## for each test instance
    for i_te in instances_te:
        ## get the closest one and store the prediction
        closest_instance = get_closest_instance(i_te, instances_tr)
        predictions.append(closest_instance["class"])

    if options.debug:
        print(predictions)

    accuracy_te = calculate_accuracy(instances_te, predictions)
    print(f"Accuracy on test set ({len(instances_te)}  instances): {accuracy_te:.2f}")
