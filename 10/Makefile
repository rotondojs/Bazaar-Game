# Variables
PYTHON := python3.11
VENV_DIR := venv
PYTHON_BIN := $(VENV_DIR)/bin/python
BUILD_DIR := bin
SERVER_SCRIPT := xserver.py
CLIENT_SCRIPT := xclient.py
SERVER_EXEC := $(BUILD_DIR)/xserver
CLIENT_EXEC := $(BUILD_DIR)/xclient

# Default target
all: $(SERVER_EXEC) $(CLIENT_EXEC)

# Create and activate virtual environment
venv:
	@echo "Creating virtual environment..."
	@if [ ! -d "$(VENV_DIR)" ]; then \
		$(PYTHON) -m venv $(VENV_DIR); \
	fi
	@echo $(CURDIR)/.. > $(VENV_DIR)/lib/$(PYTHON)/site-packages/bazaarlibs.pth
	$(VENV_DIR)/bin/pip install -r requirements.txt

# Create the build directory
$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

# Build the server executable
$(SERVER_EXEC): $(BUILD_DIR) $(VENV_DIR)
	@echo "Building xserver with $(SERVER_SCRIPT)"
	@echo '#!/bin/bash' > $(SERVER_EXEC)
	@echo 'source $(VENV_DIR)/bin/activate' >> $(SERVER_EXEC)
	@echo 'export PYTHONPATH=$(realpath ..):$$PYTHONPATH' >> $(SERVER_EXEC)
	@echo '$(PYTHON_BIN) $(SERVER_SCRIPT) $$@' >> $(SERVER_EXEC)
	@chmod +x $(SERVER_EXEC)

$(CLIENT_EXEC): $(BUILD_DIR) $(VENV_DIR)
	@echo "Building xclient with $(CLIENT_SCRIPT)"
	@echo '#!/bin/bash' > $(CLIENT_EXEC)
	@echo 'source $(VENV_DIR)/bin/activate' >> $(CLIENT_EXEC)
	@echo 'export PYTHONPATH=$(realpath ..):$$PYTHONPATH' >> $(CLIENT_EXEC)
	@echo '$(PYTHON_BIN) $(CLIENT_SCRIPT) $$@' >> $(CLIENT_EXEC)
	@chmod +x $(CLIENT_EXEC)

# Clean build artifacts and virtual environment
clean:
	rm -rf $(BUILD_DIR) $(VENV_DIR)
