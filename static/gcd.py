def gcd(X, Y):
    XR = X 
    YR = Y
    current_state = 0b01
    
    print("s0:")
    print(f"XR = {XR}, YR = {YR}")
    if XR > 0:
        current_state +=  1

    print(f"(XR > 0) = {1 if XR > 0 else 0}\t\t\t({XR} > 0)")

    print(f"(XR >= YR) = {1 if XR >= YR else 0}\t\t\t({XR} >= {YR})")
    if (XR >= YR):
        current_state += 1

    print(f"current state: {bin(current_state)[2:].zfill(2)}\n")

    while XR > 0:
        
        if XR < YR:
            
            TEMPR = YR
            YR = XR
            XR = TEMPR
            current_state = 0b01
            print("s1: ")
            print(f"swap: XR = {XR}, YR= {YR}")
            if XR > 0:
                current_state +=  1

            print(f"(XR > 0) = {1 if XR > 0 else 0}\t\t\t({XR} > 0)")

            print(f"(XR >= YR) = {1 if XR >= YR else 0}\t\t\t({XR} >= {YR})")
            if (XR >= YR):
                current_state += 1

            print(f"current state: {bin(current_state)[2:].zfill(2)}\n")
            

        print("s2: ")
        print(f"substract: XR = {XR} - {YR} = ", end="")
        XR = XR - YR
        print(f"{XR}, YR = {YR}")
        current_state = 0b01
        
        

        if XR > 0:
            current_state +=  1

        print(f"(XR > 0) = {1 if XR > 0 else 0}\t\t\t({XR} > 0)")
        print(f"(XR >= YR) = {1 if XR >= YR else 0}\t\t\t({XR} >= {YR})")
        
        if (XR >= YR):
            current_state += 1

        print(f"current state: {bin(current_state)[2:].zfill(2)}\n")
       

    print(f"YR = {YR}")


gcd(15, 20)