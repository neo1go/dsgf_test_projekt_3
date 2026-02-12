import os 
import robot

def start_robot_tests():
    print("Starte Robot Tests...")
    results_dir = os.path.join(os.getcwd(), "Results")
    os.makedirs(results_dir, exist_ok=True)

    robot.run(
        "Tests/robot_tests_seperated.robot",
        outputdir=results_dir,
        loglevel ="error"  # trace, debug, info, warn, error, none
    )
