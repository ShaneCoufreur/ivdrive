with open("app/models/vehicle.py", "r") as f:
    data = f.read()

new_relationships = """    battery_health_records: Mapped[list["BatteryHealth"]] = relationship(
        back_populates="user_vehicle", cascade="all, delete-orphan", lazy="noload"
    )
    power_usage_records: Mapped[list["PowerUsage"]] = relationship(
        back_populates="user_vehicle", cascade="all, delete-orphan", lazy="noload"
    )
    charging_curves: Mapped[list["ChargingCurve"]] = relationship(
        back_populates="user_vehicle", cascade="all, delete-orphan", lazy="noload"
    )
"""

if "battery_health_records: Mapped" not in data:
    # insert before ConnectionState to keep it together
    data = data.replace('    connection_states: Mapped[list["ConnectionState"]]', new_relationships + '\n    connection_states: Mapped[list["ConnectionState"]]')
    with open("app/models/vehicle.py", "w") as f:
        f.write(data)
        print("Vehicle updated.")
