"""
Main application for P40 Telemetry Gauge.
Provides toggle between telemetry display and benchmark mode.
"""

import argparse
import os
import time
import random
from hid_controller import HIDController
from gauge_renderer import create_gauge, save_gauge_svg


def get_telemetry_metrics():
    """
    Get simulated GPU telemetry metrics.
    In a real implementation, this would call local API or hardware sensors.

    Returns:
        Dictionary with TDP, temperature, VRAM usage, and token rate.
    """
    # Simulate realistic values for NVIDIA Tesla P40
    return {
        "tdp": random.uniform(100, 250),      # Watts
        "temperature": random.uniform(30, 80), # Celsius
        "vram_used": random.uniform(2000, 22000), # MB (out of 24576 MB)
        "vram_total": 24576,                  # MB
        "token_rate": random.uniform(10, 50)  # Tokens per second
    }


def run_benchmark():
    """
    Run a simulated benchmark to measure token generation speed.
    In a real implementation, this would run actual model inference.

    Returns:
        Token rate in tokens per second.
    """
    # Simulate benchmark workload
    time.sleep(2)  # Simulate 2 seconds of work
    # Return a token rate that varies based on simulated load
    return random.uniform(15, 45)


def main():
    parser = argparse.ArgumentParser(description='P40 Telemetry Gauge for Thermalright LCD')
    parser.add_argument('--mode', choices=['telemetry', 'benchmark'], default='telemetry',
                        help='Mode to run: telemetry (real-time metrics) or benchmark (manual benchmark)')
    parser.add_argument('--interval', type=float, default=1.0,
                        help='Update interval in seconds for telemetry mode')
    parser.add_argument('--output-dir', default='.',
                        help='Directory to save gauge SVGs (for debugging)')
    args = parser.parse_args()

    # Initialize HID controller (stub - actual HID communication would be implemented here)
    controller = HIDController()
    # Note: In a real implementation, you would connect to the device:
    # if not controller.connect():
    #     print("Warning: Could not connect to HID device. Running in simulation mode.")

    # Ensure output directory exists
    os.makedirs(args.output_dir, exist_ok=True)

    if args.mode == 'telemetry':
        print("Running in telemetry mode. Press Ctrl+C to exit.")
        print(f"Updating gauges every {args.interval} seconds. Saving SVGs to {args.output_dir}")
        try:
            while True:
                metrics = get_telemetry_metrics()
                # Calculate VRAM usage percentage
                vram_percent = (metrics['vram_used'] / metrics['vram_total']) * 100

                # Create gauges for each metric
                tdp_gauge = create_gauge(
                    metrics['tdp'],
                    min_val=0,
                    max_val=300,
                    label="TDP",
                    units="W"
                )
                temp_gauge = create_gauge(
                    metrics['temperature'],
                    min_val=0,
                    max_val=100,
                    label="Temperature",
                    units="°C"
                )
                vram_gauge = create_gauge(
                    vram_percent,
                    min_val=0,
                    max_val=100,
                    label="VRAM Usage",
                    units="%"
                )
                token_gauge = create_gauge(
                    metrics['token_rate'],
                    min_val=0,
                    max_val=100,
                    label="Token Rate",
                    units="tok/s"
                )

                # Save gauges to files (for debugging and potential HID transmission)
                save_gauge_svg(
                    metrics['tdp'],
                    0, 300,
                    "TDP",
                    "W",
                    output_path=os.path.join(args.output_dir, "tdp_gauge.svg")
                )
                save_gauge_svg(
                    metrics['temperature'],
                    0, 100,
                    "Temperature",
                    "°C",
                    output_path=os.path.join(args.output_dir, "temp_gauge.svg")
                )
                save_gauge_svg(
                    vram_percent,
                    0, 100,
                    "VRAM Usage",
                    "%",
                    output_path=os.path.join(args.output_dir, "vram_gauge.svg")
                )
                save_gauge_svg(
                    metrics['token_rate'],
                    0, 100,
                    "Token Rate",
                    "tok/s",
                    output_path=os.path.join(args.output_dir, "token_gauge.svg")
                )

                # Print to console for monitoring
                print(f"TDP: {metrics['tdp']:.1f}W | "
                      f"Temp: {metrics['temperature']:.1f}°C | "
                      f"VRAM: {vram_percent:.1f}% | "
                      f"Token: {metrics['token_rate']:.1f} tok/s")

                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\nTelemetry mode stopped.")
    else:  # benchmark mode
        print("Running benchmark...")
        token_rate = run_benchmark()
        print(f"Benchmark complete. Token rate: {token_rate:.1f} tok/s")

        # Create and save benchmark gauge
        benchmark_gauge = create_gauge(
            token_rate,
            min_val=0,
            max_val=100,
            label="Benchmark Token Rate",
            units="tok/s"
        )
        save_gauge_svg(
            token_rate,
            0, 100,
            "Benchmark Token Rate",
            "tok/s",
            output_path=os.path.join(args.output_dir, "benchmark_gauge.svg")
        )
        print(f"Benchmark gauge saved to {os.path.join(args.output_dir, 'benchmark_gauge.svg')}")


if __name__ == "__main__":
    main()