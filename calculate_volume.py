import math
from datetime import datetime

SPECIFIC_GRAVITY = 0.718
CO2 = 0
N2 = 0
PRESSURE_BASE = 14.65
PSIG_ADDEND = 14.73
TB = 60

LOG = True

def log_decorator(func):
    def decorator():
        start = datetime.now()
        results = func()
        end = datetime.now()
        if LOG:
            print("{}: \n\tfunction: {}\n\tduration: {}".format(datetime.now(),func.__name__,end-start))
        return results
    return decorator 

def calculate_volume(orifice_size, tube_bore, diff, psig, temp, specific_gravity=SPECIFIC_GRAVITY, co2=CO2, n2=N2):
    ld = log_decorator #decorate any parameter-less function with @ld to log information
    def get_c():
        def get_fb_b(): #needed for get_E() and all get_ko's inside of get_fb()
            return orifice_size / tube_bore
        def get_E():#needed for get_ko_1() inside of get_fb() and get_fr_b() inside of get_fr()
            def get_B():
                return 530/(tube_bore**0.5)
            b = get_fb_b()
            return orifice_size*(830-5000*b+9000*(b**2)-4200*(b**3)+get_B())
        def get_fb():
            def get_ko_1():
                def get_ko_2():
                    def get_ko_3():
                        def get_ko_4():
                            def get_ko_5():
                                return 0.5993+(0.007/tube_bore)+((0.364+(0.076/(tube_bore**0.5)))*get_fb_b()**4)
                            def get_temp_5():
                                def get_temp_6():
                                    return (0.07+0.5 / tube_bore)-get_fb_b()
                                temp_6 = get_temp_6()
                                return 0 if (temp_6 < 0) else (temp_6**2.5)
                            return get_ko_5()+0.4*((1.6-1/tube_bore)**5)*get_temp_5()
                        def get_temp_3():
                            def get_temp_4():
                                return 0.5 - get_fb_b()
                            temp_4 = get_temp_4()
                            return 0 if (temp_4 < 0) else (temp_4 ** 1.5)
                        return get_ko_4() -(0.009+0.034/tube_bore)*get_temp_3()
                    def get_temp_1():
                        def get_temp_2():
                            return get_fb_b() - 0.7
                        temp_2 = get_temp_2()
                        return 0 if (temp_2 < 0) else (temp_2 ** 2.5)
                    return get_ko_3()+(65/(tube_bore**2)+3)*get_temp_1()
                return get_ko_2()/(1+((15*get_E())/(1000000*orifice_size)))
            return 338.178 * (orifice_size ** 2) * get_ko_1()
        def get_fr():
            def get_fr_b():
                def get_k():
                    return 0.604/(1-get_fb_b()**4)**0.5
                return get_E()/(12835*orifice_size*get_k())
            return 1+get_fr_b()/get_hw_pf()
        def get_Y():
            def get_x2():
                return diff/(27.707*(psig + PSIG_ADDEND))
            x2 = get_x2()
            return ((1+x2)**0.5)-((0.41+0.35*(get_fb_b()**4))*(x2/1.3*((1+x2)**0.5)))
        def get_fpb():
            return 14.73/PRESSURE_BASE
        def get_ftb():
            return (TB+459.67)/519.67
        def get_ftf():
            return math.sqrt(519.67/(temp+459.67))
        def get_fgr():
            return math.sqrt(1/specific_gravity)
        def get_fpv():
            AC3 = psig
            AC4 = temp
            AC5 = specific_gravity
            AC6 = n2
            AC7 = co2
            AC8 = 156.47*AC3
            AC9 = 160.8-(7.22*AC5)+(AC7-0.392*AC6)
            AC10 = round(AC8/AC9,1)
            AC11 = 226.29*(AC4+460)
            AC12 = 99.15+(211.9*AC5)-(AC7+1.681*AC6)
            AC13 = round((AC11/AC12)-460,1)
            AC14 = (AC10+14.7)/1000
            AC15 = (AC13+460)/500
            AC16 = (0.0330378/(AC15**2))-(0.0221323/(AC15**3))+(0.0161353/(AC15**5))
            AC17 = round(((0.265827/(AC15**2))+(0.0457697/(AC15**4))-(0.133185/AC15))/AC16,9)
            AC18 = round((3-(AC16*(AC17**2)))/(9*AC16*(AC14**2)),7)
            AC19 = round(1-(0.00075*(AC14**2.3))*(2-(2.718281828**(-20*(1.09-AC15))))-(1.317*((1.09-AC15)**4)*(AC14*(1.69-(AC14**2)))),4)
            AC20 = round(((9*AC17-(2*AC16*(AC17**3)))/(54*AC16*(AC14**3)))-(AC19/(2*AC16*(AC14**2))),7)
            AC21 = round((AC20+((AC20**2)+(AC18**3))**(1/2))**(1/3),8)
            AC22 = ((AC18/AC21)-AC21+(AC17/(3*AC14)))**(1/2)
            AC23 = 1+(0.00132/(AC15**3.25))
            return round(AC22/AC23,4)
        fb = get_fb()#l7
        fr = get_fr()#l8
        Y = get_Y()#l9
        fpb = get_fpb()#l10
        ftb = get_ftb()#l11
        ftf = get_ftf()#l12
        fgr = get_fgr()#l13
        fpv = get_fpv()#l14
        #c = l7 * l8 * l9 * l10 * l11 * l12 * l13 * l14
        return fb * fr * Y * fpb * ftb * ftf * fgr * fpv
    def get_hw_pf():
        return math.sqrt(diff) * math.sqrt(psig + PSIG_ADDEND)
    volume = get_c() * get_hw_pf() * 24 / 1000
    return volume

if __name__ == '__main__':
    volume = calculate_volume(2.5,4,524,320,120,SPECIFIC_GRAVITY,CO2,N2)
    print(volume)

