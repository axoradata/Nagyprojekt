using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using NagyprojektBackend.Data;
using NagyprojektBackend.Models;

namespace NagyprojektBackend.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    [Authorize]
    public class RfidController : ControllerBase
    {
        private readonly AppDbContext _db;
        public RfidController(AppDbContext db) => _db = db;

        [HttpGet]
        public IActionResult GetAll() => Ok(_db.RfidTags.ToList());

        [HttpPost]
        public IActionResult Create([FromBody] RfidTag tag)
        {
            _db.RfidTags.Add(tag);
            _db.SaveChanges();
            return CreatedAtAction(nameof(Get), new { id = tag.Id }, tag);
        }

        [HttpGet("{id}")]
        public IActionResult Get(int id)
        {
            var tag = _db.RfidTags.Find(id);
            if (tag == null) return NotFound();
            return Ok(tag);
        }

        [HttpPut("{id}/activate")]
        public IActionResult Activate(int id, [FromQuery] bool active)
        {
            var tag = _db.RfidTags.Find(id);
            if (tag == null) return NotFound();
            tag.Active = active;
            _db.SaveChanges();
            return Ok(tag);
        }
    }
}
