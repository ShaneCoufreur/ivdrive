with open("app/models/telemetry.py", "r") as f:
    data = f.read()

new_classes = """

class BatteryHealth(Base):
    __tablename__ = "battery_health"
    __table_args__ = (
        UniqueConstraint("user_vehicle_id", "captured_at", name="uq_battery_health_vehicle_captured"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_vehicle_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user_vehicles.id", ondelete="CASCADE"), nullable=False, index=True
    )
    captured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    
    # 12V Battery
    twelve_v_battery_voltage: Mapped[float | None] = mapped_column(Float)
    twelve_v_battery_soc: Mapped[float | None] = mapped_column(Float)
    twelve_v_battery_soh: Mapped[float | None] = mapped_column(Float)
    
    # HV Battery
    hv_battery_voltage: Mapped[float | None] = mapped_column(Float)
    hv_battery_current: Mapped[float | None] = mapped_column(Float)
    hv_battery_temperature: Mapped[float | None] = mapped_column(Float)
    hv_battery_soh: Mapped[float | None] = mapped_column(Float)
    hv_battery_degradation_pct: Mapped[float | None] = mapped_column(Float)
    
    # Cell level data (could be stored as JSON or average/min/max)
    cell_voltage_min: Mapped[float | None] = mapped_column(Float)
    cell_voltage_max: Mapped[float | None] = mapped_column(Float)
    cell_voltage_avg: Mapped[float | None] = mapped_column(Float)
    cell_temperature_min: Mapped[float | None] = mapped_column(Float)
    cell_temperature_max: Mapped[float | None] = mapped_column(Float)
    cell_temperature_avg: Mapped[float | None] = mapped_column(Float)
    imbalance_mv: Mapped[float | None] = mapped_column(Float)
    
    user_vehicle: Mapped["UserVehicle"] = relationship(back_populates="battery_health_records")


class PowerUsage(Base):
    __tablename__ = "power_usage"
    __table_args__ = (
        UniqueConstraint("user_vehicle_id", "captured_at", name="uq_power_usage_vehicle_captured"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_vehicle_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user_vehicles.id", ondelete="CASCADE"), nullable=False, index=True
    )
    captured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    
    # Consumption metrics
    total_power_kw: Mapped[float | None] = mapped_column(Float)
    motor_power_kw: Mapped[float | None] = mapped_column(Float)
    hvac_power_kw: Mapped[float | None] = mapped_column(Float)
    auxiliary_power_kw: Mapped[float | None] = mapped_column(Float)
    battery_heater_power_kw: Mapped[float | None] = mapped_column(Float)
    
    user_vehicle: Mapped["UserVehicle"] = relationship(back_populates="power_usage_records")


class ChargingCurve(Base):
    __tablename__ = "charging_curves"
    __table_args__ = (
        UniqueConstraint("user_vehicle_id", "captured_at", name="uq_charging_curves_vehicle_captured"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_vehicle_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user_vehicles.id", ondelete="CASCADE"), nullable=False, index=True
    )
    session_id: Mapped[int | None] = mapped_column(ForeignKey("charging_sessions.id", ondelete="CASCADE"))
    captured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    
    soc_pct: Mapped[float | None] = mapped_column(Float)
    power_kw: Mapped[float | None] = mapped_column(Float)
    voltage_v: Mapped[float | None] = mapped_column(Float)
    current_a: Mapped[float | None] = mapped_column(Float)
    battery_temp_celsius: Mapped[float | None] = mapped_column(Float)
    charger_temp_celsius: Mapped[float | None] = mapped_column(Float)
    
    user_vehicle: Mapped["UserVehicle"] = relationship()

"""

if "class BatteryHealth" not in data:
    with open("app/models/telemetry.py", "a") as f:
        f.write(new_classes)
        print("Models appended.")
