# Working only for MacOS atm

# Install pyenv
if brew list | grep -q '^pyenv-virtualenv$'; then
  echo "pyenv-virtualenv is already installed."
else
  echo "Installing pyenv-virtualenv..."
  brew install pyenv-virtualenv
fi

# Add env paths to the bash profile
if cat ~/.bash_profile | grep -q 'pyenv init'; then
  echo "bash_profile is already configured."
else
  echo "Configuring bash_profile for pyenv and pyenv-virtualenv..."
  echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\n  eval "$(pyenv virtualenv-init -)"\nfi' >> ~/.bash_profile
fi

# Reinit the .bash_profile
. ~/.bash_profile

# Install the right python version
if pyenv versions | grep -q '3.8.2'; then
  echo "Python 3.8.2 is already installed."
else
  echo "Installing Python 3.8.2..."
  pyenv install 3.8.2
fi

# Setup the kisa python environment
if pyenv versions | grep -q 'kisa$'; then
  echo "kisa environment already exists."
else
  echo "Creating kisa environment..."
  pyenv virtualenv 3.8.2 kisa
fi

# Activate the environment and generate .python-version file
pyenv activate kisa
pyenv local kisa

# Upgrade pip version
if pip list --outdated 2>/dev/null | grep -q '^pip'; then
  echo "Upgrading pip to the latest stable version..."
  pip install --upgrade pip
fi

# Install pip dependencies
pip install -r requirements.txt

# Profit