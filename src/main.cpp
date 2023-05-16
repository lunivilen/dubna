#include <vector>
#include <get_data.h>

using namespace std;

int main() {
    vector<vector<vector<vector<float>>>> result;
    result.push_back(get_data(R"(C:\Users\ilya2\Desktop\C++\dubna\src\data\event0.txt)", 10));
    return 0;
}
