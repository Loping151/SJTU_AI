import os

# path to data file
file_dir = os.path.dirname(__file__)
data_path = os.path.join(file_dir, "stream_data_dgim.txt")
edge_path1 = os.path.join(file_dir, "edge1.txt")
edge_path2 = os.path.join(file_dir, "edge2.txt")

class DGIM:
    def __init__(self, filepath, windowsize, maxtime = None):
        '''init DGIM for specific file

        Args:
            filepath (str): data file path
            windowsize (int): 
            maxtime (int, optional): timestamp modulo N. Defaults to None.
        '''
        self.fileHandler = open(filepath, 'r')
        self.windowSize = windowsize
        self.buckets = [] # list[list]
        self.timeMod = maxtime if maxtime else windowsize << 2
        self.timestamp = 0
    
    def update(self, x):
        '''update when a new bit come in

        Args:
            x (str): new bit, can be "1" or "0"
        '''
        ### TODO
        ### maintaining 1 or 2 of each size bucket
        if x == '1':
            if len(self.buckets) == 0:
                self.buckets.append([self.timestamp])
            else:
                self.buckets[0].append(self.timestamp)
                
        for k in range(len(self.buckets)):
            if len(self.buckets[k]) == 3:
                ri, self.buckets[k] = self.buckets[k][1], self.buckets[k][2:]
                if len(self.buckets) <= k+1:
                    self.buckets.append([ri] if self.windowSize + (self.timestamp + (self.timeMod if ri > self.timestamp else 0)) > self.timestamp else [])
                else:
                    self.buckets[k+1] += [ri] if self.windowSize + (self.timestamp + (self.timeMod if ri > self.timestamp else 0)) > self.timestamp else []
                
        ### end of TODO

    
    def run(self):
        '''simulate the process of stream data
        '''
        
        f = self.fileHandler
        x = f.read(2).strip()
        while x:
            # x can be string "1" or "0"
            self.update(x)
        
            # get next bit
            self.timestamp = (self.timestamp + 1) % self.timeMod
            x = f.read(2).strip()
            
    def count(self, k=None):
        '''count the number of 1-bits in last k bits

        Args:
            k (int, optional): . Defaults to the windowsize.

        Returns:
            int: count results
        '''
        
    
        if k is None:
            k = self.windowSize
        
        result = 0
        
        ### TODO
        ### return floor(1 / 2) if the last bucket is zero
        b_end = 0
        for nk in range(len(self.buckets)):
            for ri in self.buckets[nk]:
                t = self.timestamp - ri - k
                if ri > self.timestamp:
                    t += self.timeMod
                if t > 0:
                    continue
                elif t == 0:
                    b_end = 0 # I'm not sure what means floor(1/2). Isn't it 0?
                else:
                    result += 2**nk
                    b_end = 2**nk

        result -= (b_end // 2)
        return result
        
        ### end of TODO
    
    
if __name__ == "__main__":
    
    dgim = DGIM(filepath=data_path, windowsize=1000)

    dgim.run()
    
    # current window
    print("the number of 1-bits in current windows: ")
    print(f"   {dgim.count()}")
    
    # last 500 and 200
    print("the number of 1-bits in the last 500 and 200 bits of the stream")
    print(f"   {dgim.count(k=500)}")
    print(f"   {dgim.count(k=200)}")
    
    print("edge cases:")
    dgim1 = DGIM(filepath=edge_path1, windowsize=1000)

    dgim1.run()
    
    print(f"    {dgim1.count()}")
    dgim2 = DGIM(filepath=edge_path2, windowsize=1000)
    
    dgim2.run()
    print(f"    {dgim2.count()}")
    