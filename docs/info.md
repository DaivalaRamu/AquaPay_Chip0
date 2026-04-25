## How it works

The AquaPay Chip is a smart water dispensing system controlled by coin inputs.

When a user inserts a coin (₹1, ₹2, ₹5, ₹10), the system selects a predefined amount of water (liters) along with a maximum dispensing time.

The design is implemented using a Finite State Machine (FSM) with four states:
- IDLE: Waits for coin input
- SET: Determines target liters and time limit based on the coin
- DISP: Turns ON the valve and dispenses water
- DONE: Stops dispensing and resets the system

A flow sensor provides pulses corresponding to water flow. Each pulse increases the liter count.

The system stops dispensing water when:
- The required number of liters is reached, OR
- The maximum allowed time is exceeded

The valve control signal is provided as output, along with the current liters count in binary form.


## How to test

1. Apply clock and reset:
   - `clk` → system clock
   - `rst_n` → active-low reset

2. Provide inputs using `ui_in`:
   - `ui_in[0]` → ₹1 coin
   - `ui_in[1]` → ₹2 coin
   - `ui_in[2]` → ₹5 coin
   - `ui_in[3]` → ₹10 coin
   - `ui_in[4]` → flow sensor pulse

3. Insert a coin by setting the corresponding input HIGH for one clock cycle.

4. Simulate water flow by toggling `ui_in[4]` (flow sensor pulses).

5. Observe outputs on `uo_out`:
   - `uo_out[0]` → valve ON/OFF
   - `uo_out[7:1]` → liters count (binary)

6. Verify:
   - Correct liters dispensed for each coin
   - Valve turns OFF after reaching target or timeout


## External hardware

- Push buttons or switches for coin inputs
- Water flow sensor (pulse output type)
- Solenoid valve (controlled using valve_on output)
- LEDs or display to monitor output signals (optional)
