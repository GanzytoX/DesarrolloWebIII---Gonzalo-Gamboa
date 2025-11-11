import { useState, useEffect, useCallback } from "react";
import "./App.css";

export default function App() {
  // ==================== STATE MANAGEMENT ====================
  const [numbers, setNumbers] = useState(["", ""]);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const [history, setHistory] = useState([]);
  const [completeHistory, setCompleteHistory] = useState([]);

  const [operationFilter, setOperationFilter] = useState("all");
  const [dateFilter, setDateFilter] = useState("");
  const [sortBy, setSortBy] = useState("date");
  const [sortDirection, setSortDirection] = useState("desc");

  // ==================== NUMBER MANAGEMENT ====================
  const addNumber = () => setNumbers((prev) => [...prev, ""]);
  const removeNumber = (index) =>
    setNumbers((prev) =>
      prev.length <= 2 ? prev : prev.filter((_, i) => i !== index)
    );
  const updateNumber = (index, value) =>
    setNumbers((prev) => {
      const copy = [...prev];
      copy[index] = value;
      return copy;
    });

  // ==================== UTILS ====================
  const formatDate = (dateString) => dateString;

  const getOperationSymbol = (operation) => {
    const symbols = {
      sum: "+",
      subtract: "-",
      substract: "-", // alias común
      multiply: "×",
      multiplication: "×", // alias
      divide: "÷",
      division: "÷", // alias
      // legacy
      suma: "+",
      resta: "-",
      multiplicacion: "×",
    };
    return symbols[operation] || "?";
  };

  const normalizeOperation = (op) => {
    const map = {
      substract: "subtract",
      multiplication: "multiply",
      multiplicacion: "multiply",
      division: "divide",
      suma: "sum",
      resta: "subtract",
    };
    return map[op] || op;
  };

  // ==================== FILTERS (DECLARAR ANTES) ====================
  const applyFilters = useCallback(
    (data = completeHistory) => {
      let filtered = [...data];

      if (operationFilter !== "all") {
        filtered = filtered.filter(
          (op) =>
            normalizeOperation(op.operation) ===
            normalizeOperation(operationFilter)
        );
      }

      if (dateFilter) {
        filtered = filtered.filter((op) =>
          (op.date || "").includes(dateFilter)
        );
      }

      filtered.sort((a, b) => {
        let A, B;
        if (sortBy === "date") {
          const parse = (s = "") => {
            const [d = "", t = "00:00"] = s.split(" ");
            const [day = "01", mon = "01", year = "1970"] = d.split("/");
            const [hh = "00", mm = "00"] = t.split(":");
            return new Date(year, Number(mon) - 1, day, hh, mm);
          };
          A = parse(a.date);
          B = parse(b.date);
        } else {
          A = a.result;
          B = b.result;
        }
        return sortDirection === "asc" ? (A > B ? 1 : -1) : A < B ? 1 : -1;
      });

      setHistory(filtered);
    },
    [operationFilter, dateFilter, sortBy, sortDirection, completeHistory]
  );

  // ==================== HISTORY (DECLARAR DESPUÉS) ====================
  const getHistory = useCallback(async () => {
    try {
      const res = await fetch("http://localhost:8089/calculator/history");
      const data = await res.json();
      if (res.ok) {
        const list = data.history || [];
        setCompleteHistory(list);
        applyFilters(list);
      }
    } catch (err) {
      console.error("Error getting history:", err);
    }
  }, [applyFilters]);

  // ==================== VALIDATION & OPS ====================
  const validateNumbers = () => {
    if (numbers.some((n) => n === "" || n == null)) {
      setError("Please complete all numbers");
      setResult(null);
      return false;
    }
    if (numbers.length < 2) {
      setError("At least 2 numbers are required");
      setResult(null);
      return false;
    }
    return true;
  };

  const performOperation = async (operation) => {
    if (!validateNumbers()) return;
    setIsLoading(true);
    setError(null);
    setResult(null);
    try {
      const params = numbers
        .map((n) => `numbers=${encodeURIComponent(n)}`)
        .join("&");
      const res = await fetch(
        `http://localhost:8089/calculator/${operation}?${params}`
      );
      const data = await res.json();
      if (!res.ok)
        throw new Error(data.error || data.detail || "Error in operation");
      setResult(data.result);
      getHistory();
    } catch (err) {
      setError(err.message);
      setResult(null);
    } finally {
      setIsLoading(false);
    }
  };

  // ==================== EFFECTS ====================
  useEffect(() => {
    getHistory();
  }, [getHistory]);

  useEffect(() => {
    applyFilters();
  }, [applyFilters]);

  // ==================== CLEAR FILTERS ====================
  const clearFilters = () => {
    setOperationFilter("all");
    setDateFilter("");
    setSortBy("date");
    setSortDirection("desc");
  };

  // ==================== RENDER ====================
  return (
    <div className="app-container">
      <div className="calculator-card">
        <h1 className="app-title">Calculator</h1>
        <div className="input-container">
          <div className="numbers-header">
            <span>Numbers for operation:</span>
            <button
              className="add-number-btn"
              onClick={addNumber}
              type="button">
              + Add Number
            </button>
          </div>

          {numbers.map((number, index) => (
            <div key={index} className="number-row">
              <input
                type="number"
                className="number-input"
                value={number}
                onChange={(e) => updateNumber(index, e.target.value)}
                placeholder={`Number ${index + 1}`}
              />
              {numbers.length > 2 && (
                <button
                  className="remove-number-btn"
                  onClick={() => removeNumber(index)}
                  type="button">
                  ×
                </button>
              )}
            </div>
          ))}
        </div>

        <div className="operations-grid">
          <button
            className="operation-btn"
            onClick={() => performOperation("sum")}
            disabled={isLoading}>
            + Add
          </button>
          <button
            className="operation-btn"
            onClick={() => performOperation("substract")}
            disabled={isLoading}>
            - Subtract
          </button>
          <button
            className="operation-btn"
            onClick={() => performOperation("multiply")}
            disabled={isLoading}>
            × Multiply
          </button>
          <button
            className="operation-btn"
            onClick={() => performOperation("divide")}
            disabled={isLoading}>
            ÷ Divide
          </button>
        </div>

        <div className="result-container">
          {isLoading && <div>Calculating...</div>}
          {error && <div className="error-text">{error}</div>}
          {result !== null && !error && !isLoading && (
            <div className="result-text">Result: {result}</div>
          )}
          {result === null && !error && !isLoading && (
            <div style={{ color: "#6b7280" }}>Select an operation</div>
          )}
        </div>
      </div>

      <div className="history-card">
        <h3 className="history-title">Operation History</h3>

        <div className="filters-container">
          <div className="filter-row">
            <div className="filter-group">
              <label className="filter-label">Operation type:</label>
              <select
                className="filter-select"
                value={operationFilter}
                onChange={(e) => setOperationFilter(e.target.value)}>
                <option value="all">All</option>
                <option value="sum">Sum</option>
                <option value="subtract">Subtract</option>
                <option value="multiply">Multiply</option>
                <option value="divide">Divide</option>
              </select>
            </div>

            <div className="filter-group">
              <label className="filter-label">Date (dd/mm/yyyy):</label>
              <input
                type="text"
                className="filter-input"
                value={dateFilter}
                onChange={(e) => setDateFilter(e.target.value)}
                placeholder="Ex: 22/09/2025"
              />
            </div>
          </div>

          <div className="filter-row">
            <div className="filter-group">
              <label className="filter-label">Sort by:</label>
              <select
                className="filter-select"
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}>
                <option value="date">Date</option>
                <option value="result">Result</option>
              </select>
            </div>

            <div className="filter-group">
              <label className="filter-label">Direction:</label>
              <select
                className="filter-select"
                value={sortDirection}
                onChange={(e) => setSortDirection(e.target.value)}>
                <option value="desc">Descending</option>
                <option value="asc">Ascending</option>
              </select>
            </div>

            <button className="clear-filters-btn" onClick={clearFilters}>
              Clear Filters
            </button>
          </div>
        </div>

        <ul className="history-list">
          {history.length > 0 ? (
            history.map((op, i) => (
              <li key={i} className="history-item">
                <div className="operation-info">
                  <div className="operation-text">
                    {op.numbers
                      ? op.numbers.join(
                          ` ${getOperationSymbol(op.operation)} `
                        ) + ` = ${op.result}`
                      : op.operandos
                      ? op.operandos.join(
                          ` ${getOperationSymbol(op.operation)} `
                        ) + ` = ${op.result}`
                      : `${op.a} ${getOperationSymbol(op.operation)} ${
                          op.b
                        } = ${op.result}`}
                  </div>
                  <div className="operation-type">
                    {normalizeOperation(op.operation)}
                  </div>
                </div>
                <div className="operation-date">{formatDate(op.date)}</div>
              </li>
            ))
          ) : (
            <div className="no-history">No operations in history</div>
          )}
        </ul>
      </div>
    </div>
  );
}
