
class KirilStemmer:

    # offset into b # offset to end of stemmed word
    # unit of size whereby b is increased
    def __init__(self):
        self._b = []
        self._i = 0
        self._i_end = 0
        self._j = 0
        self._k = 0

    # *
    # * Add a character to the word being stemmed.  When you are finished
    # * adding characters, you can call stem(void) to stem the word.
    #
    def add(self, ch):
        self._b.append(ch)
        self._i += 1

    # *
    # * Adds wLen characters to the word being stemmed contained in a portion
    # * of a char[] array. This is like repeated calls of add(char ch), but
    # * faster.
    #
    def add(self, w, wLen):
        c = 0
        for c in range(wLen):
            self._b.append(w[c])
            self._i += 1

    # *
    # * After a word has been stemmed, it can be retrieved by toString(),
    # * or a reference to the internal buffer can be retrieved by getResultBuffer
    # * and getResultLength (which is generally more efficient.)
    #
    def toString(self):
        temp = ""
        for t in range(self._i_end):
            temp += self._b[t]
        return temp

    # *
    # * Returns the length of the word resulting from the stemming process.
    #
    def getResultLength(self):
        return self._i_end

    # *
    # * Returns a reference to a character buffer containing the results of
    # * the stemming process.  You also need to consult getResultLength()
    # * to determine the length of the result.
    #
    def getResultBuffer(self):
        return self._b

    # cons(i) is true <=> b[i] is a consonant.
    def cons(self, i):
        if self._b[i] == 'a' or self._b[i] == 'e' or self._b[i] == 'i' or self._b[i] == 'o' or self._b[i] == 'u':
            return False
        elif self._b[i] == 'y':
            return True if (i == 0) else not self.cons(i - 1)
        else:
            return True

    # m() measures the number of consonant sequences between 0 and j. if c is
    # a consonant sequence and v a vowel sequence, and <..> indicates arbitrary
    # presence,
    #
    # <c><v>       gives 0
    # <c>vc<v>     gives 1
    # <c>vcvc<v>   gives 2
    # <c>vcvcvc<v> gives 3
    # ....
    #
    def m(self):
        n = 0
        i = 0
        while True:
            if i > self._j:
                return n
            if not self.cons(i):
                break
            i += 1
        i += 1
        while True:
            while True:
                if i > self._j:
                    return n
                if self.cons(i):
                    break
                i += 1
            i += 1
            n += 1
            while True:
                if i > self._j:
                    return n
                if not self.cons(i):
                    break
                i += 1
            i += 1

    # vowelinstem() is true <=> 0,...j contains a vowel
    def vowelinstem(self):
        for i in range(self._j):
            if not self.cons(i):
                return True
        return False

    # doublec(j) is true <=> j,(j-1) contain a double consonant.
    def doublec(self, j):
        if j < 1:
            return False
        if self._b[j] != self._b[j - 1]:
            return False
        return self.cons(j)

    # cvc(i) is true <=> i-2,i-1,i has the form consonant - vowel - consonant
    # and also if the second c is not w,x or y. this is used when trying to
    # restore an e at the end of a short word. e.g.
    #
    # cav(e), lov(e), hop(e), crim(e), but
    # snow, box, tray.
    #
    #
    def cvc(self, i):
        if i < 2 or not self.cons(i) or self.cons(i - 1) or not self.cons(i - 2):
            return False
        ch = self._b[i]
        if ch == 'w' or ch == 'x' or ch == 'y':
            return False
        return True

    def ends(self, s):
        l = len(s)
        o = self._k - l + 1
        if o < 0:
            return False
        for i in range(l):
            if self._b[o + i] != s[i]:
                return False
        self._j = self._k - l
        return True

    # setto(s) sets (j+1),...k to the characters in the string s, readjusting
    # k.
    def setto(self, s):
        l = len(s)
        o = self._j + 1
        i = 0
        for i in range(l):
            self._b[o + i] = s[i]
        self._k = self._j + l

    # r(s) is used further down.
    def r(self, s):
        if self.m() > 0:
            self.setto(s)

    # step1() gets rid of plurals and -ed or -ing. e.g.
    #
    # caresses  ->  caress
    # ponies    ->  poni
    # ties      ->  ti
    # caress    ->  caress
    # cats      ->  cat
    #
    # feed      ->  feed
    # agreed    ->  agree
    # disabled  ->  disable
    #
    # matting   ->  mat
    # mating    ->  mate
    # meeting   ->  meet
    # milling   ->  mill
    # messing   ->  mess
    #
    # meetings  ->  meet
    #
    #
    def step1(self):
        if self._b[self._k] == 's':
            if self.ends("sses"):
                self._k -= 2
            elif self.ends("ies"):
                self.setto("i")
            elif self._b[self._k - 1] != 's':
                self._k -= 1
        if self.ends("eed"):
            if self.m() > 0:
                self._k -= 1
        elif (self.ends("ed") or self.ends("ing")) and self.vowelinstem():
            self._k = self._j
            if self.ends("at"):
                self.setto("ate")
            elif self.ends("bl"):
                self.setto("ble")
            elif self.ends("iz"):
                self.setto("ize")
            elif self.doublec(self._k):
                self._k -= 1
                ch = self._b[self._k]
                if ch == 'l' or ch == 's' or ch == 'z':
                    self._k += 1
            elif self.m() == 1 and self.cvc(self._k):
                self.setto("e")

    # step2() turns terminal y to i when there is another vowel in the stem.
    def step2(self):
        if self.ends("y") and self.vowelinstem():
            self._b[self._k] = 'i'

    # step3() maps double suffices to single ones. so -ization ( = -ize plus
    # -ation) maps to -ize etc. note that the string before the suffix must give
    # m() > 0.
    def step3(self):
        if self._k == 0:
            return  # For Bug 1
        if self._b[self._k - 1] == 'a':
            if self.ends("ational"):
                self.r("ate")
            elif self.ends("tional"):
                self.r("tion")
        elif self._b[self._k - 1] == 'c':
            if self.ends("enci"):
                self.r("ence")
            elif self.ends("anci"):
                self.r("ance")
        elif self._b[self._k - 1] == 'e':
            if self.ends("izer"):
                self.r("ize")
        elif self._b[self._k - 1] == 'l':
            if self.ends("bli"):
                self.r("ble")
            elif self.ends("alli"):
                self.r("al")
            elif self.ends("entli"):
                self.r("ent")
            elif self.ends("eli"):
                self.r("e")
            elif self.ends("ousli"):
                self.r("ous")
        elif self._b[self._k - 1] == 'o':
            if self.ends("ization"):
                self.r("ize")
            elif self.ends("ation"):
                self.r("ate")
            elif self.ends("ator"):
                self.r("ate")
        elif self._b[self._k - 1] == 's':
            if self.ends("alism"):
                self.r("al")
            elif self.ends("iveness"):
                self.r("ive")
            elif self.ends("fulness"):
                self.r("ful")
            elif self.ends("ousness"):
                self.r("ous")
        elif self._b[self._k - 1] == 't':
            if self.ends("aliti"):
                self.r("al")
            elif self.ends("iviti"):
                self.r("ive")
            elif self.ends("biliti"):
                self.r("ble")
        elif self._b[self._k - 1] == 'g':
            if self.ends("logi"):
                self.r("log")

    # step4() deals with -ic-, -full, -ness etc. similar strategy to step3.
    def step4(self):
        if self._b[self._k] == 'e':
            if self.ends("icate"):
                self.r("ic")
            elif self.ends("ative"):
                self.r("")
            elif self.ends("alize"):
                self.r("al")
        elif self._b[self._k] == 'i':
            if self.ends("iciti"):
                self.r("ic")
        elif self._b[self._k] == 'l':
            if self.ends("ical"):
                self.r("ic")
            elif self.ends("ful"):
                self.r("")
        elif self._b[self._k] == 's':
            if self.ends("ness"):
                self.r("")

    # step5() takes off -ant, -ence etc., in context <c>vcvc<v>.
    def step5(self):
        if self._k == 0:
            return
        tempk1 = self._k - 1
        if self._b[tempk1] == 'a':
            if self.ends("al"):
                pass
            else:
                return
        elif self._b[tempk1] == 'c':
            if self.ends("ance"):
                pass
            elif self.ends("ence"):
                pass
            else:
                return
        elif self._b[tempk1] == 'e':
            if self.ends("er"):
                pass
            else:
                return
        elif self._b[tempk1] == 'i':
            if self.ends("ic"):
                pass
            else:
                return
        elif self._b[tempk1] == 'l':
            if self.ends("able"):
                pass
            elif self.ends("ible"):
                pass
            else:
                return
        elif self._b[tempk1] == 'n':
            if self.ends("ant"):
                pass
            elif self.ends("ement"):
                pass
            elif self.ends("ment"):
                pass
            # element etc. not stripped before the m
            elif self.ends("ent"):
                pass
            else:
                return
        elif self._b[tempk1] == 'o':
            if self.ends("ion") and self._j >= 0 and (self._b[self._j] == 's' or self._b[self._j] == 't'):
                pass
            # j >= 0 fixes Bug 2
            elif self.ends("ou"):
                pass
            else:
                return
        elif self._b[tempk1] == 's':
            if self.ends("ism"):
                pass
            else:
                return
        elif self._b[tempk1] == 't':
            if self.ends("ate"):
                pass
            elif self.ends("iti"):
                pass
            else:
                return
        elif self._b[tempk1] == 'u':
            if self.ends("ous"):
                pass
            else:
                return
        elif self._b[tempk1] == 'v':
            if self.ends("ive"):
                pass
            else:
                return
        elif self._b[tempk1] == 'z':
            if self.ends("ize"):
                pass
            else:
                return
        else:
            return
        if self.m() > 1:
            self._k = self._j

    # step6() removes a final -e if m() > 1.
    def step6(self):
        self._j = self._k
        if self._b[self._k] == 'e':
            a = self.m()
            if a > 1 or a == 1 and not self.cvc(self._k - 1):
                self._k -= 1
        if self._b[self._k] == 'l' and self.doublec(self._k) and self.m() > 1:
            self._k -= 1

    # * Stem the word placed into the Stemmer buffer through calls to add().
    # * Returns true if the stemming process resulted in a word different
    # * from the input.  You can retrieve the result with
    # * getResultLength()/getResultBuffer() or toString().\

    def stem(self):
        self._k = self._i - 1
        if self._k > 1:
            self.step1()
            self.step2()
            self.step3()
            self.step4()
            self.step5()
            self.step6()
        self._i_end = self._k + 1
        self._i = 0

    def stemString(self, string):
        length = len(string)
        w = []
        ret = []
        a = 0
        while a != -1:
            ch = string[a]
            a += 1
            if a == length:
                a = -1
            if ch.isalpha() or ch == '_' or ch == '-':
                j = 0
                while True:
                    ch = ch.lower()
                    w.append(ch)
                    if j < 257:
                        j += 1
                    if a != -1:
                        ch = string[a]
                        a += 1
                    if a == length:
                        a = -1
                        w.append(ch)
                        if j < 257:
                            j += 1
                    if not ch.isalpha() and not (ch == '_') and not (ch == '-') or a == -1:
                        self.add(w, j)
                        self.stem()
                        ret.append(self.toString())
                        break
        return ret

    def stemOneWord(self, word):
        self._b = []
        self._i = 0
        self._i_end = 0
        sl = self.stemString(word)
        if len(sl) > 0:
            return sl[0]
        else:  # TBD: inefficient: FIX
            return ""
