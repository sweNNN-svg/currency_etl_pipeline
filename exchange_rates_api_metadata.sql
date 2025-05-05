CREATE TABLE exchange_rates (
	id SERIAL PRIMARY KEY,
	base_currency VARCHAR(3) NOT NULL,
	target_currency VARCHAR(3) NOT NULL,
	rate DECIMAL(19,6) NOT NULL,
	last_updated TIMESTAMPTZ NOT NULL,
	UNIQUE(base_currency, target_currency)
);

CREATE TABLE api_metadata (
    id SERIAL PRIMARY KEY,
    update_timestamp TIMESTAMPTZ NOT NULL,
    next_update_timestamp TIMESTAMPTZ NOT NULL,
    api_status VARCHAR(20) NOT NULL,
    base_currency VARCHAR(3) NOT NULL
);