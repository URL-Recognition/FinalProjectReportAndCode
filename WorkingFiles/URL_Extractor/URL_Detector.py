class URL_Detector:

    CHARACTER_RANGE = [0,255]
    #WORD_LENGTHS = [0,5,10,15,20]
    WORD_LENGTHS = []
    #SPECIAL_CASES = []
    SPECIAL_CASES = ['https','.com','.org','.gov','.edu']
    EXT_INDEXES = [len(WORD_LENGTHS),len(SPECIAL_CASES)]
    BIN_SIZE = CHARACTER_RANGE[1]-CHARACTER_RANGE[0] + EXT_INDEXES[0] + EXT_INDEXES[1]
    URL_prob = []
    URL_hist = [0 for i in range(BIN_SIZE)]
    #URL_hist2 = [0 for i in range(BIN_SIZE)]
    NonURL_prob = []
    NonURL_hist = [0 for i in range(BIN_SIZE)]
    #NonURL_hist2 = [0 for i in range(BIN_SIZE)]

    def set_character_range(self,min,max):
        self.CHARACTER_RANGE = [min,max]

    # Read input file to get list of strings
    def read_input(self, filename):
        with open(filename) as f:
            content = f.readlines()
            f.close()
        content = [x.strip() for x in content]

        return content

    # The histogram of letters in a string, special cases and length
    #Histogram order: [word_length(0,5,10,15),special cases,letters]
    def get_histogram(self, input_str):

        #Ignore case
        input_str = input_str.lower()

        #Initialize histogram
        hist = [0 for i in range(self.BIN_SIZE)]

        #Fill first parts of histogram with word lengths
        word_length = len(input_str)
        for i in range(0, self.EXT_INDEXES[0]-1):
            if word_length > self.WORD_LENGTHS[i]:
                hist[i] = 1

        #Fill next part with histogram of special case occurences
        for i in range(0, self.EXT_INDEXES[1]-1):
            hist[self.EXT_INDEXES[0]+i] = input_str.count(self.SPECIAL_CASES[i])

        # Count char occurrences
        for c in input_str:
            hist[self.EXT_INDEXES[0] + self.EXT_INDEXES[1] + ord(c) - self.CHARACTER_RANGE[0]] += 1

        return hist

    # Get histogram of training set fileName
    def training_hist(self, filename):
        data = self.read_input(filename)

        hist = [0 for i in range(self.BIN_SIZE)]
        #hist2 = [0 for i in range(self.BIN_SIZE)]

        for val in data:
            width = len(val)

            h1 = self.get_histogram(val)
            #h2 = self.get_histogram(val[width/2+1:])

            # Add values from ›
            hist = [x + y for x, y in zip(h1, hist)]
            #hist2 = [x + y for x, y in zip(h2, hist2)]

        return hist

    def calc_probabilities(self, histogram):
        total = sum(histogram) + len(histogram)
        probs = [(i + 1) / total for i in histogram]
        return probs

    def train_classifier(self, filename, is_url):

        training = self.training_hist(filename)
        if is_url:
            self.URL_hist = [x + y for x, y in zip(self.URL_hist, training)]
        else:
            self.NonURL_hist = [x + y for x, y in zip(self.NonURL_hist, training)]

    def set_probabilities(self):
        self.URL_prob = self.calc_probabilities(self.URL_hist)
        self.NonURL_prob = self.calc_probabilities(self.NonURL_hist)

    def perform_training(self,url_file,non_url_file):
        self.train_classifier(url_file,True)
        self.train_classifier(non_url_file,False)
        self.set_probabilities()

    def pre_classify(self, string):
        if len(string) < 5:
            return False
        if string.count('.') < 1:
            return False
        return True


    def classify(self, string):

        if not self.pre_classify(string):
            return -1

        if len(self.URL_prob) < 1 or len(self.NonURL_prob) < 1:
            print('The classifier must be trained first!')

        # Calculate probabilities
        url_prob = .5
        not_prob = .5
        for c in string:
            v = ord(c)
            if(v > self.CHARACTER_RANGE[1]):#Skip characters that are outside desired range
                continue
            url_prob *= self.URL_prob[v - self.CHARACTER_RANGE[0]]
            not_prob *= self.NonURL_prob[v - self.CHARACTER_RANGE[0]]

        return url_prob - not_prob

    def classify_array(self, strings):

        urls = []

        for string in strings:
            prob = self.classify(string)
            if prob > 0:
                urls.append(string)

        return urls
