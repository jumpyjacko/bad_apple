CXX = clang++
CXXFLAGS = -Wall -Wextra -std=c++20 -O2
DEBUG_CXXFLAGS = -Wall -Wextra -std=c++20 -O0 -g

LIBS = -lgtest -lgtest_main

TARGET_DIR_RELEASE = target/release
TARGET_DIR_DEBUG   = target/debug

TARGET = $(TARGET_DIR_RELEASE)/main
DEBUG_TARGET = $(TARGET_DIR_DEBUG)/main_debug

SRCS = $(wildcard *.cpp)
OBJS = $(patsubst %.cpp,$(TARGET_DIR_RELEASE)/%.o,$(SRCS))
DEBUG_OBJS = $(patsubst %.cpp,$(TARGET_DIR_DEBUG)/%.debug.o,$(SRCS))

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(OBJS) $(LIBS)

$(TARGET_DIR_RELEASE)/%.o: %.cpp
	@mkdir -p $(TARGET_DIR_RELEASE)
	$(CXX) $(CXXFLAGS) -c $< -o $@

debug: $(DEBUG_TARGET)

$(DEBUG_TARGET): $(DEBUG_OBJS)
	$(CXX) $(DEBUG_CXXFLAGS) -o $(DEBUG_TARGET) $(DEBUG_OBJS) $(LIBS)

$(TARGET_DIR_DEBUG)/%.debug.o: %.cpp
	@mkdir -p $(TARGET_DIR_DEBUG)
	$(CXX) $(DEBUG_CXXFLAGS) -c $< -o $@

clean:
	rm -rf $(TARGET_DIR_RELEASE) $(TARGET_DIR_DEBUG)

run: $(TARGET)
	./$(TARGET)

.PHONY: all debug clean run
