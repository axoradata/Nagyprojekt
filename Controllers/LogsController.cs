using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using NagyprojektBackend.Data;
using NagyprojektBackend.Models;
using System.Linq;

namespace NagyprojektBackend.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    [Authorize]
    public class LogsController : ControllerBase
    {
        private readonly AppDbContext _db;
        public LogsController(AppDbContext db) => _db = db;

        [HttpGet]
        public IActionResult GetAll([FromQuery] int page = 1, [FromQuery] int pageSize = 50)
        {
            var query = _db.Logs.OrderByDescending(l => l.Timestamp);
            var total = query.Count();
            var items = query.Skip((page - 1) * pageSize).Take(pageSize).ToList();
            return Ok(new { total, items });
        }

        [HttpPost]
        public IActionResult Create([FromBody] LogEntry log)
        {
            log.Timestamp = DateTime.UtcNow;
            _db.Logs.Add(log);
            _db.SaveChanges();
            return CreatedAtAction(nameof(GetById), new { id = log.Id }, log);
        }

        [HttpGet("{id}")]
        public IActionResult GetById(int id)
        {
            var l = _db.Logs.Find(id);
            if (l == null) return NotFound();
            return Ok(l);
        }
    }
}
