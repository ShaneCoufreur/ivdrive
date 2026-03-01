with open("app/models/telemetry.py", "a") as f:
    f.write("""

class ChargingPower(Base):
    __tablename__ = "charging_powers"
    __table_args__ = (
        UniqueConstraint("user_vehicle_id", "first_date", name="uq_charging_powers_vehicle_first"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_vehicle_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user_vehicles.id", ondelete="CASCADE"), nullable=False, index=True
    )
    first_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    last_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    power: Mapped[float | None] = mapped_column(Float)

    user_vehicle: Mapped["UserVehicle"] = relationship()


class DriveRangeEstimatedFull(Base):
    __tablename__ = "drive_ranges_estimated_full"
    __table_args__ = (
        UniqueConstraint("drive_id", "first_date", name="uq_dr_estimated_full_drive_first"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    drive_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("drives.id", ondelete="CASCADE"), nullable=False, index=True
    )
    first_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    last_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    range_estimated_full: Mapped[float | None] = mapped_column(Float)

    drive: Mapped["Drive"] = relationship()


class DriveConsumption(Base):
    __tablename__ = "drive_consumptions"
    __table_args__ = (
        UniqueConstraint("drive_id", "first_date", name="uq_dc_drive_first"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    drive_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("drives.id", ondelete="CASCADE"), nullable=False, index=True
    )
    first_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    last_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    consumption: Mapped[float | None] = mapped_column(Float)

    drive: Mapped["Drive"] = relationship()


class ClimatizationState(Base):
    __tablename__ = "climatization_states"
    __table_args__ = (
        UniqueConstraint("user_vehicle_id", "first_date", name="uq_climatization_states_vehicle_first"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_vehicle_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user_vehicles.id", ondelete="CASCADE"), nullable=False, index=True
    )
    first_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    last_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    state: Mapped[str | None] = mapped_column(String(30))

    user_vehicle: Mapped["UserVehicle"] = relationship()


class OutsideTemperature(Base):
    __tablename__ = "outside_temperatures"
    __table_args__ = (
        UniqueConstraint("user_vehicle_id", "first_date", name="uq_outside_temp_vehicle_first"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_vehicle_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user_vehicles.id", ondelete="CASCADE"), nullable=False, index=True
    )
    first_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    last_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    outside_temperature: Mapped[float | None] = mapped_column(Float)

    user_vehicle: Mapped["UserVehicle"] = relationship()


class BatteryTemperature(Base):
    __tablename__ = "battery_temperatures"
    __table_args__ = (
        UniqueConstraint("user_vehicle_id", "first_date", name="uq_battery_temp_vehicle_first"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_vehicle_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user_vehicles.id", ondelete="CASCADE"), nullable=False, index=True
    )
    first_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    last_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    battery_temperature: Mapped[float | None] = mapped_column(Float)

    user_vehicle: Mapped["UserVehicle"] = relationship()


class WeconnectError(Base):
    __tablename__ = "weconnect_errors"
    __table_args__ = (
        UniqueConstraint("user_vehicle_id", "datetime", name="uq_weconnect_errors_vehicle_dt"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_vehicle_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user_vehicles.id", ondelete="CASCADE"), nullable=False, index=True
    )
    datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    error_text: Mapped[str | None] = mapped_column(String(255))

    user_vehicle: Mapped["UserVehicle"] = relationship()

""")
