#include <iostream>
#include <string>
int main() {
    std::string l;
    if (!std::getline(std::cin, l)) return 1;
    auto p = l.find('\t');
    if (p == std::string::npos) return 1;
    std::cout << l.substr(0, p) << '\t' << l.substr(p + 1) << ">C++\n";
}
