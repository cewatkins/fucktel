# Makefile for CP437 Telnet Client (C version)

CC = gcc
CFLAGS = -Wall -Wextra -O2 -std=c99
LDFLAGS = 
TARGET = fucktel
EXAMPLE_TARGET = examples_c
TEST_TARGET = test_cp437

# Source files
SOURCES = fucktel.c cp437_decode.c
EXAMPLE_SOURCES = examples.c
TEST_SOURCES = test_cp437.c cp437_decode.c
OBJECTS = $(SOURCES:.c=.o)
EXAMPLE_OBJECTS = $(EXAMPLE_SOURCES:.c=.o)
TEST_OBJECTS = $(TEST_SOURCES:.c=.o)

# Default target
all: $(TARGET) $(EXAMPLE_TARGET)

# Build main telnet client
$(TARGET): $(OBJECTS)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

# Build examples
$(EXAMPLE_TARGET): $(EXAMPLE_OBJECTS)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

# Build tests
$(TEST_TARGET): $(TEST_OBJECTS)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

# Compile object files
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

# Clean build artifacts
clean:
	rm -f $(OBJECTS) $(EXAMPLE_OBJECTS) $(TEST_OBJECTS) $(TARGET) $(EXAMPLE_TARGET) $(TEST_TARGET)

# Install (optional)
install: $(TARGET)
	install -m 755 $(TARGET) /usr/local/bin/

# Uninstall (optional)
uninstall:
	rm -f /usr/local/bin/$(TARGET)

# Run tests
test: $(TEST_TARGET)
	./$(TEST_TARGET)

# Test compilation
build-test: $(TARGET)
	@echo "Build successful! Run with: ./$(TARGET) hostname [port]"

# Help
help:
	@echo "CP437 Telnet Client - C version"
	@echo ""
	@echo "Available targets:"
	@echo "  all         - Build telnet client and examples (default)"
	@echo "  test        - Build and run tests"
	@echo "  clean       - Remove build artifacts"
	@echo "  install     - Install to /usr/local/bin (requires root)"
	@echo "  uninstall   - Remove from /usr/local/bin (requires root)"
	@echo "  build-test  - Build and verify compilation"
	@echo "  help        - Show this help message"
	@echo ""
	@echo "Usage after building:"
	@echo "  ./$(TARGET) hostname [port]"
	@echo "  ./$(EXAMPLE_TARGET)"
	@echo "  ./$(TEST_TARGET)"

.PHONY: all clean install uninstall test build-test help
