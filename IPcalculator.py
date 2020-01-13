#Eli Decker
# CS331 Computer Networks
#09/24/19

# example:
# Enter IP address: 192.168.0.1
#  Enter prefix length: 24


#  Subnet address:     192.168.0.0
#  First host:         192.168.0.1
#  Last host:          192.168.0.254
#  Broadcast address:  192.168.0.255
#  Subbet mask:        255.255.255.0

import sys
from re import match as re_match

def removeDots(s):
    """ Returns True is string is a number. """
    return s.replace('.','',1).isdigit()

def checkRange(s):
    ''' check if there is 4 bytes to the IP address
    and that they are in the proper range (0 to 255)'''
    fourBytes = s.split('.')
    if len(fourBytes) < 4:
        print("IP Address is too short")
        return False
    else:
        for byte in fourBytes:
            try:
                if int(byte) < 0:
                    print("IP address value: ", byte," is less than 0")
                    return False
                elif int(byte) > 255:
                    print("IP address value: ", byte," is greater than 255")
                    return False
                else:
                    return fourBytes
            except:
                print("IP address value: ", byte," is not a number")
                return False
            

def is_number(s):
    """ Returns True is string is a number. """
    if s.isdigit():
        if int(s) < 0:
            print("Prefix length is less than zero")
            return False
        elif int(s) > 32:
            print("Prefix length is greater than 32")
            return False
        else:
            return s
    else:
        print("Prefix must be an integer")
        return False
        

    # return False

def errorChecking(s):
    isWrong = False
    while isWrong == False:
        flag = checkRange(s)
        if flag != False:
            isWrong = True
        else:
            print("Please submit IP address in proper format")
            s = input("Enter IP address: ")
    return flag

def prefixErrorChecking(s):
    isWrong = False
    while isWrong == False:
        flag = is_number(s)
        if flag != False:
            isWrong = True
        else:
            print("Please submit prefix length in proper format")
            s = input("Enter prefix length: ")
    return flag

def findSubnetAddress(address, prefix):
    zeros = "00000000000000000000000000000000"
    ones = "11111111111111111111111111111111"

    # creates binary mask from string of ones and zeros
    mask = ones[:prefix] + zeros[prefix:]

    addressString = ''
    for byte in address:
        addressString += str(byte)
    addressBinary = addressString

    # bitwise 'AND' operation
    subnetAddress = str(format(int(addressBinary,2) & int(mask,2), '032b') )

    subnetAddress2 = list(map(''.join, zip(*[iter(subnetAddress)]*8)))

    addressString = ''
    for byte in subnetAddress2:
        addressString += str(int(byte, 2)) + "."
    
    tempInt = int(subnetAddress2[3], 2) + 1
    lastByte = [str(format(tempInt, '08b'))]
    firstHost = subnetAddress2[:3] + lastByte

    firstHostAddressString = ''
    for byte in firstHost:
        firstHostAddressString += str(int(byte,2)) + "."


    addressString = addressString[:-1]
    firstHostAddressString = firstHostAddressString[:-1]

    return addressString, firstHostAddressString

def findBroadcastAddress(address, prefix):
    ones = "11111111111111111111111111111111"

    addressString = ''
    for byte in address:
        addressString += str(byte)

    broadcastAddress = addressString[:prefix] + ones[prefix:]

    # list of four 8 bit strings
    broadcastAddress2 = list(map(''.join, zip(*[iter(broadcastAddress)]*8)))

    addressString = ''
    for byte in broadcastAddress2:
        addressString += str(int(byte,2)) + "."
    
    tempInt = int(broadcastAddress2[3], 2) - 1
    lastByte = [str(format(tempInt, '08b'))]
    lastHost = broadcastAddress2[:3] + lastByte

    lastHostAddressString = ''
    for byte in lastHost:
        lastHostAddressString += str(int(byte,2)) + "."


    addressString = addressString[:-1]
    lastHostAddressString = lastHostAddressString[:-1]

    return addressString, lastHostAddressString

def findSubnetMask(address, prefix):
    zeros = "00000000000000000000000000000000"
    ones = "11111111111111111111111111111111"
    # 32 bit string
    mask = ones[:prefix] + zeros[prefix:]

    # list of four 8 bit strings
    mask2 = list(map(''.join, zip(*[iter(mask)]*8)))

    addressString = ''
    for byte in mask2:
        addressString += str(int(byte,2)) + "."
    addressString = addressString[:-1]
    return addressString


def main(argv):
    ''' Get the IP address from user '''
    txt = input("Enter IP address: ")

    
    '''perform some error checking '''
    byteList = errorChecking(txt)

    # print("Is this what you just said? ", string)
    binaryList = []
    for byte in byteList:
        tempInt = int(byte)
        binaryList.append(format(tempInt, '08b'))
    # print("TESTING")
    # print(binaryList)

    prefixOriginal = input("Enter prefix length: ")
    prefix = int(prefixErrorChecking(prefixOriginal))

    subnet_address, first_host = findSubnetAddress(binaryList, prefix)
    broadcast_address, last_host = findBroadcastAddress(binaryList, prefix)
    subnet_mask = findSubnetMask(binaryList, prefix)

    print("Subnet address: {0:15} {1}".format("", subnet_address))
    print("First host: {0:19} {1}".format("", first_host))
    print("Last host: {0:20} {1}".format("", last_host))
    print("Broadcast address: {0:12} {1}".format("", broadcast_address))
    print("Subnet mask: {0:18} {1}".format("", subnet_mask))



if __name__ == "__main__":
    main(sys.argv)