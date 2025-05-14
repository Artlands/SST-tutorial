.PHONY: src

CC=${RVCC}
ARCH=rv64imafdc
RV_OBJDUMP=riscv64-unknown-elf-objdump

RISCV_GCC_OPTS ?= -mcmodel=medany -static -std=gnu17 -O0 -ffast-math -fno-common -fno-builtin-printf -march=$(ARCH) -mabi=lp64d
CFLAGS = -I$(XBGAS_RUNTIME)/include  -I$(REV)/common/syscalls

ifeq "$(RVCC)" "riscv64-unknown-elf-gcc"
	RISCV_GCC_OPTS += -fno-tree-loop-distribute-patterns
endif

# Source files excluding util.c
SRCS = $(filter-out $(UTIL_SRC), $(wildcard *.c))

# Object files for each source
OBJS = $(SRCS:.c=.o)

# Executables for each source
EXES = $(SRCS:.c=.exe)

all:$(EXES)

%.exe: %.o
	$(CC) $(CFLAGS) $(RISCV_GCC_OPTS)  -o $@ $^ -L$(XBGAS_RUNTIME)/lib -lxbrtime -lm

# Rule to compile source files into object files
%.o:%.c
	$(CC) $(CFLAGS) $(RISCV_GCC_OPTS) -c -o $@ $<

dump: $(EXES)
	$(foreach var,$(EXES),$(RV_OBJDUMP) -d $(var) > $(var).dump;)

clean:
	rm -Rf *.exe *.dump *.o

#-- EOF