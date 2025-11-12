# Makefile for CP437 Telnet Client (C version)

CC = gcc
CFLAGS = -Wall -Wextra -O2 -std=c99
LDFLAGS = 
TARGET = fucktel
EXAMPLE_TARGET = examples_c

# Source files
SOURCES = fucktel.c
EXAMPLE_SOURCES = examples.c
OBJECTS = $(SOURCES:.c=.o)
EXAMPLE_OBJECTS = $(EXAMPLE_SOURCES:.c=.o)

# Default target
all: $(TARGET) $(EXAMPLE_TARGET)

# Build main telnet client
$(TARGET): $(OBJECTS)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

# Build examples
$(EXAMPLE_TARGET): $(EXAMPLE_OBJECTS)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

# Compile object files
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

# Clean build artifacts
clean:
	rm -f $(OBJECTS) $(EXAMPLE_OBJECTS) $(TARGET) $(EXAMPLE_TARGET)

# Install (optional)
install: $(TARGET)
	install -m 755 $(TARGET) /usr/local/bin/

# Uninstall (optional)
uninstall:
	rm -f /usr/local/bin/$(TARGET)

# Test compilation
test: $(TARGET)
	@echo "Build successful! Run with: ./$(TARGET) hostname [port]"

# Help
help:
	@echo "CP437 Telnet Client - C version"
	@echo ""
	@echo "Available targets:"
	@echo "  all       - Build telnet client and examples (default)"
	@echo "  clean     - Remove build artifacts"
	@echo "  install   - Install to /usr/local/bin (requires root)"
	@echo "  uninstall - Remove from /usr/local/bin (requires root)"
	@echo "  test      - Build and verify compilation"
	@echo "  help      - Show this help message"
	@echo ""
	@echo "Usage after building:"
	@echo "  ./$(TARGET) hostname [port]"
	@echo "  ./$(EXAMPLE_TARGET)"

.PHONY: all clean install uninstall test help
