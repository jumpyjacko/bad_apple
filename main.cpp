#include <chrono>
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <thread>

int main() {
    std::string line;
    std::ifstream file ("bad_apple_32x24.txt");

    std::string first_line;
    int x, y, s;
    if (std::getline(file, first_line)) {
        std::istringstream iss(first_line);
        if (iss >> x >> y >> s) {
            std::cout << "Parsed metadata! " << x << ", " << y << ". With sub height: " << s << '\n';
        } else {
            std::cout << "Failed to parse metadata" << '\n';
            exit(1);
        }
    }

    std::cout << "\033[2J\033[H";

    int count {};

    while (std::getline(file, line)) {
        using std::chrono::operator""ms;
        auto now {std::chrono::steady_clock::now()};
        
        if (count == y + s - 1 ) {
            std::cout << "\n\033[3mAlstroemeria Records - Bad Apple!! (feat. nomico)" << '\n';
            std::cout << "Original music by ZUN" << '\n';
            std::cout << "Original video by あにら on nico nico\033[0m" << '\n';
            
            count = 0;
            
            auto frame_time = now + 33.2ms;
            
            std::this_thread::sleep_until(frame_time);
            now = std::chrono::steady_clock::now();
            
            std::cout << "\033[2J\033[H";
            continue;
        }

        count++;
        
        std::string out;

        if (count > y) {
            std::cout << line << '\n';
        } else {
            for (const char c : line) {
                if (c == '0') {
                    out += ". ";
                } else {
                    out += "##";
                }
            }
            std::cout << out << "\n";
        }
    }
    
    return 0;
}
