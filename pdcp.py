Num_SN_Bits = 0
SN_Bits = 0
Next_PDCP_TX_SN = 0
headerCompOn = 0
def PDCP_setup():
  global headerCompOn
  global SN_Bits
  global Next_PDCP_TX_SN
  global Num_SN_Bits
  Num_SN_Bits = [5, 7, 12, 15, 18]
  SN_Bits = Num_SN_Bits[2]
  Next_PDCP_TX_SN = 0
  headerCompOn = 1
  file = open("header.txt","w")
  file.write('')
  file.close()
  print('PDCP Initiated')



def receive_PDCP_PDU(dataStream): #Receive PDCP_PDU, TO BE CALLED BY UDP ON SENDING SIDE
  global Next_PDCP_TX_SN
  global SN_Bits
  Max_PDCP_SN = 2**(SN_Bits)-1
  Next_PDCP_TX_SN += 1
  if Next_PDCP_TX_SN > Max_PDCP_SN:
    Next_PDCP_TX_SN = 1
  to_RLC = setHeader(dataStream, Next_PDCP_TX_SN, SN_Bits)
  print('PDCP SDU: '+to_RLC)         #RLC function to be called here


def headerCompression(dataStream, Next_PDCP_TX_SN):
  if Next_PDCP_TX_SN == 1:            # For first time transmission
    print('First Packet. Hence header not compressed!')
    return dataStream
  else:
    dataStream = dataStream[2:]
    out = '0xff' + dataStream[4:8] + dataStream[20:28] + dataStream[48:]
    print('Header Compressed Data: '+ out)
    return out


def setHeader(dataStream, Next_PDCP_TX_SN, SN_Bits):
  if dataStream[:2]!='0x':
    dataStream = '0x'+ dataStream          #if '0x' not present in input

  if headerCompOn == 1:
    dataStream = headerCompression(dataStream, Next_PDCP_TX_SN)

  if SN_Bits == 5:              #FOR THE CASE OF SRB
    outputStream = hex(Next_PDCP_TX_SN)[2:].zfill(2) + str(dataStream[2:]) + '0CF36E17'
    return outputStream

  elif SN_Bits == 7:              #FOR THE CASE OF DRB-7
    outputStream = hex(0b10000000 | Next_PDCP_TX_SN) + str(dataStream[2:])
    return outputStream[2:]

  elif SN_Bits == 12:              #FOR THE CASE OF DRB-12
    outputStream = hex(0b1000000000000000 | Next_PDCP_TX_SN) + str(dataStream[2:])
    return outputStream[2:]

  elif SN_Bits == 15:              #FOR THE CASE OF DRB-15
    outputStream = hex(0b1000000000000000 | Next_PDCP_TX_SN) + str(dataStream[2:])
    return outputStream[2:]

  elif SN_Bits == 18:              #FOR THE CASE OF DRB-18
    outputStream = hex(0b100000000000000000000000 | Next_PDCP_TX_SN) + str(dataStream[2:])
    return outputStream[2:]

  if SN_Bits != 5 or SN_Bits != 7 or SN_Bits != 12 or SN_Bits != 15 or SN_Bits != 18:
    raise Exception("Supported SN Bits is limited to 5, 7, 12, 15 and 18!")


def send_PDCP_PDU(dataStream): #send PDCP_PDU, TO BE CALLED BY RLC ON RECEIVING SIDE
  removeHeader(dataStream)
                              #CALL a function given by UDP team here


def removeHeader(PDCP_PDU):
  global SN_Bits
  if PDCP_PDU[:2]=='0x':
    PDCP_PDU = PDCP_PDU[2:]          #if '0x' present in input
  if SN_Bits == 5:              #FOR THE CASE OF SRB
    out1 = PDCP_PDU[2:]
    out = out1[:-8]
    hexSN = PDCP_PDU[:2]
    intSN = int(hexSN, 16)

  elif SN_Bits == 7:              #FOR THE CASE OF DRB-7
    out = PDCP_PDU[2:]
    hexSN = PDCP_PDU[:2]
    intSN = int(hexSN, 16) - 128

  elif SN_Bits == 12:              #FOR THE CASE OF DRB-12
    out = PDCP_PDU[4:]
    hexSN = PDCP_PDU[:4]
    intSN = int(hexSN, 16) - 32768

  elif SN_Bits == 15:              #FOR THE CASE OF DRB-15
    out = PDCP_PDU[4:]
    hexSN = PDCP_PDU[:4]
    intSN = int(hexSN, 16) - 32768

  elif SN_Bits == 18:              #FOR THE CASE OF DRB-18
    out = PDCP_PDU[6:]
    hexSN = PDCP_PDU[:6]
    intSN = int(hexSN, 16) - 8388608

  # elif DataChannel == 0:
  #   raise Exception("Control Channel not supported!")
  # if SN_Bits != 5 or SN_Bits != 7 or SN_Bits != 12 or SN_Bits != 15 or SN_Bits != 18:
  #   raise Exception("Supported SN Bits is limited to 5, 7, 12, 15 and 18!")

  if headerCompOn == 1:
    out = headerDecompression(out, intSN)
  return (out, intSN)

def headerDecompression(dataStream, Next_PDCP_TX_SN):
  if Next_PDCP_TX_SN == 1:            # For first time transmission
    header = dataStream[:56]
    file = open("header.txt","w")
    file.write(header)
    file.close()
    return dataStream
  elif dataStream[:2] == 'ff':
    dataStream = dataStream[2:]
    file = open("header.txt","r+")
    header = file.read()
    file.close()
    out = header[:4] + dataStream[:4] + header[8:20] + dataStream[4:12] + header[28:48] + dataStream[12:]
    return out

PDCP_setup()
#receive_PDCP_PDU('0x123456789abcdef123456789abcdef123456789abcdef123456789abcdef123456789abcdef123456789abcdef123456789abcdef')
