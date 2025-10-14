import { useState, useEffect, useCallback } from "react";
import "./App.css";

export default function App() {
  // ==================== STATE MANAGEMENT ====================

  // Calculator states
  const [numbers, setNumbers] = useState(["", ""]);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  // History states
  const [history, setHistory] = useState([]);
  const [completeHistory, setCompleteHistory] = useState([]);

  // Filter states
  const [operationFilter, setOperationFilter] = useState("all");
  const [dateFilter, setDateFilter] = useState("");
  const [sortBy, setSortBy] = useState("date");
  const [sortDirection, setSortDirection] = useState("desc");

  console.log("App rendering, numbers:", numbers);

  // ==================== NUMBER MANAGEMENT FUNCTIONS ====================

  const addNumber = () => {
    setNumbers((prev) => [...prev, ""]);
  };

  const removeNumber = (index) => {
    setNumbers((prev) => {
      if (prev.length <= 2) return prev;
      return prev.filter((_, i) => i !== index);
    });
  };

  const updateNumber = (index, value) => {
    setNumbers((prev) => {
      const copy = [...prev];
      copy[index] = value;
      return copy;
    });
  };

  // ==================== VALIDATION FUNCTIONS ====================

  const validateNumbers = () => {
    if (
      numbers.some((num) => num === "" || num === null || num === undefined)
    ) {
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

  // ==================== CALCULATOR OPERATIONS ====================

  const performOperation = async (operation) => {
    if (!validateNumbers()) return;

    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const params = numbers
        .map((num) => `numbers=${encodeURIComponent(num)}`)
        .join("&");
      const res = await fetch(
        `http://localhost:8089/calculator/${operation}?${params}`
      );
      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.error || data.detail || "Error in operation");
      }

      setResult(data.result);
      getHistory(); // se llama a la versión memoizada
    } catch (err) {
      setError(err.message);
      setResult(null);
    } finally {
      setIsLoading(false);
    }
  };

  // ==================== HISTORY MANAGEMENT ====================

  const getHistory = useCallback(async () => {
    try {
      const res = await fetch("http://localhost:8089/calculator/history");
      const data = await res.json();

      console.log("History data:", data);

      if (res.ok) {
        setCompleteHistory(data.history || []);
        applyFilters(data.history || []);
      }
    } catch (err) {
      console.error("Error getting history:", err);
    }
  }, [applyFilters]);

  // ==================== UTILITY FUNCTIONS ====================

  const formatDate = (dateString) => {
    return dateString;
  };

  const getOperationSymbol = (operation) => {
    const symbols = {
      // nombres "nuevos"
      sum: "+",
      subtract: "-",
      substract: "-", // alias común
      multiply: "×",
      division: "÷",
      divide: "÷",
      // nombres "viejos" o alternativos
      suma: "+",
      resta: "-",
      multiplicacion: "×",
      multiplication: "×",
    };
    return symbols[operation] || "?";
  };

  // Normaliza nombres de operación para comparar filtros y datos:
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

  // ==================== FILTER FUNCTIONS ====================

  const applyFilters = useCallback(
    (data = completeHistory) => {
      let filteredHistory = [...data];

      // Filter by operation type
      if (operationFilter !== "all") {
        filteredHistory = filteredHistory.filter(
          (op) =>
            normalizeOperation(op.operation) ===
            normalizeOperation(operationFilter)
        );
      }

      // Filter by date
      if (dateFilter) {
        filteredHistory = filteredHistory.filter((op) =>
          (op.date || "").includes(dateFilter)
        );
      }

      // Sort
      filteredHistory.sort((a, b) => {
        let valueA, valueB;

        if (sortBy === "date") {
          // Convert date dd/mm/yyyy hh:mm to Date for comparison
          const parseDate = (dateStr = "") => {
            const [datePart = "", timePart = "00:00"] = dateStr.split(" ");
            const [day = "01", month = "01", year = "1970"] =
              datePart.split("/");
            const [hours = "00", minutes = "00"] = timePart.split(":");
            return new Date(year, Number(month) - 1, day, hours, minutes);
          };
          valueA = parseDate(a.date);
          valueB = parseDate(b.date);
        } else if (sortBy === "result") {
          valueA = a.result;
          valueB = b.result;
        }

        if (sortDirection === "asc") {
          return valueA > valueB ? 1 : -1;
        } else {
          return valueA < valueB ? 1 : -1;
        }
      });

      setHistory(filteredHistory);
    },
    [operationFilter, dateFilter, sortBy, sortDirection, completeHistory]
  );

  const clearFilters = () => {
    setOperationFilter("all");
    setDateFilter("");
    setSortBy("date");
    setSortDirection("desc");
  };

  // ==================== EFFECTS ====================

  useEffect(() => {
    getHistory();
  }, [getHistory]);

  useEffect(() => {
    applyFilters();
  }, [applyFilters]);

  // ==================== RENDER ====================

  return (
    <div className="app-container">
      {/* Calculator Section */}
      <div className="calculator-card">
        <h1 className="app-title">Calculator</h1>

        {/* Number Input Section */}
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

        {/* Operations Section */}
        <div className="operations-grid">
          <button
            className="operation-btn"
            onClick={() => performOperation("sum")}
            disabled={isLoading}>
            + Add
          </button>
          <button
            className="operation-btn"
            onClick={() => performOperation("substract")} // backend usa "substract"
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

        {/* Result Section */}
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

      {/* History Section */}
      <div className="history-card">
        <h3 className="history-title">Operation History</h3>

        {/* Filter Controls */}
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

        {/* History List */}
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
