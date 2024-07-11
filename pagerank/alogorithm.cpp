#include <iostream>
using namespace std;
#include<vector>

int binary_search(vector<int>& nums, int target) {
    int left = 0 ;
    int right = nums.size() - 1;
    while (left <= right) {
        int middle = left + (right - left) / 2;
        if (nums[middle] < target) {
            left = middle + 1;
        } else if (nums[middle] > target) {
            right = middle - 1;
        } else {
            return middle;
        }
    } 
    return -1;
}


int main() {
    
    vector<int> sample = {1,2,3,4,7,9,10};
    cout << binary_search(sample,2) << endl;
    return 0;
}